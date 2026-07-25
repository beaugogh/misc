---
title: "Kubernetes 在 AI Native 时代的挑战与转型 | Jimmy Song"
source_url: "https://jimmysong.io/zh/blog/kubernetes-ai-native/"
fetched_at: "2026-07-25T08:32:49+00:00"
extraction_method: "stdlib-html-parser"
canonical_url: "https://jimmysong.io/zh/blog/kubernetes-ai-native/"
description: "探讨 Kubernetes 在 AI Native 时代面临的挑战，以及如何从 Cloud Native 迈向 AI Native，实现平台的持续相关性。"
language: "zh"
---

# Kubernetes 在 AI Native 时代的挑战与转型 | Jimmy Song

> 探讨 Kubernetes 在 AI Native 时代面临的挑战，以及如何从 Cloud Native 迈向 AI Native，实现平台的持续相关性。

## Source Metadata

- Source URL: https://jimmysong.io/zh/blog/kubernetes-ai-native/
- Canonical URL: https://jimmysong.io/zh/blog/kubernetes-ai-native/
- Fetched at: 2026-07-25T08:32:49+00:00
- Extraction method: stdlib-html-parser

## Page Content

[跳转到主要内容](https://jimmysong.io/zh/blog/kubernetes-ai-native/#main-content)[跳转到导航](https://jimmysong.io/zh/blog/kubernetes-ai-native/#navigation)[跳转到分享](https://jimmysong.io/zh/blog/kubernetes-ai-native/#social-share)[跳转到页脚](https://jimmysong.io/zh/blog/kubernetes-ai-native/#site-footer)

## Kubernetes 在 AI Native 时代的挑战与转型

探讨 Kubernetes 在 AI Native 时代面临的挑战，以及如何从 Cloud Native 迈向 AI Native，实现平台的持续相关性。

2025/09/03
•
[云原生](https://jimmysong.io/zh/categories/cloud-native)
•
21 分钟
•
7318 字
•
今年更新

Kubernetes 正如 Linux，已从“明星技术”转型成为云原生

##### 云原生（Cloud Native）

充分利用云计算优势的应用程序开发和部署方法。

的底层基础设施。它正在前台“消失”，却依然是混合算力和智能调度的核心。唯有持续进化并深度融入 AI 生态，Kubernetes 才能在新技术浪潮中保持关键地位。

随着 AI 技术的爆发式发展，基础设施被提出了前所未有的高要求。Kubernetes 作为 Cloud Native（云原生）时代的事实标准，在 AI Native
时代正面临全新的挑战：更高级的算力调度、异构资源管理、数据安全与合规，以及更加自动化和智能化的运维等。传统的云原生实践已无法完全满足 AI 工作负载的需求，Kubernetes
若想保持自身的相关性，就必须与时俱进地演化。这对于已经走过近十年发展的 Kubernetes 来说是一个重要命题——笔者自 2015 年 Kubernetes 开源伊始就开始关注并在社区布道
Kubernetes，转眼间它已经成为基础设施领域的“常青树”，如今在 AI 浪潮下是时候重新审视它的角色与前景了。

Kubernetes 在 AI Native 时代的角色正在发生转变。从前它是微服务时代的明星，被誉为“云端的操作系统”，负责在多样环境中可靠地编排容器化

##### 容器化（Containerization）

将应用程序及其依赖打包到容器中的技术。

工作负载。但 AI 原生的工作负载（尤其是生成式 AI 时代之后）有着本质的不同，可能让 Kubernetes 退居幕后成为“隐形的基础设施”——重要但不再是显性创新发生的舞台。具体而言，大型 AI
模型的训练和托管常常发生在超大规模云厂商（Hyperscaler）的专有基础设施上，很少离开那些深度集成的环境；模型推理服务则越来越多地通过 API
形式对外提供，而不是作为传统应用容器部署。此外，训练任务的调度对 GPU 感知、高吞吐的需求远超以往，往往需要借助 Kubernetes 之外的专门框架来实现。因此，AI Native
软件栈的分层方式也与云原生时代有所不同：在新的架构中，最上层是 AI Agent 和 AI 应用，其下是上下文数据管道和向量数据库等数据层，再下层是模型及其推理 API
接口，底层则是加速计算基础设施。在这样分层的体系中，如果不做出改变，Kubernetes 可能沦为背后的“底层支撑”——依然重要，但不再是创新的前台舞台。

### Kubernetes 在 AI Native 时代的挑战

什么是 Run:ai？

Run:ai 是 NVIDIA 提供的一款 Kubernetes 原生 GPU

##### GPU（图形处理器）

并行计算利器，常用于深度学习训练。

编排与优化平台，专为 AI 工作负载设计。它通过智能调度、动态分配与“GPU 分片”（fractional GPU）功能，极大提升 GPU 利用率；支持跨本地、云端与混合场景的统一管理，并可通过 API、CLI、UI 与 Kubeflow、Ray、ML-tools 等主流 AI 工具链无缝集成。详见 [NVIDIA 网站](https://www.nvidia.com/en-us/software/run-ai/)。

即使在 AI 时代，Kubernetes 仍不可或缺，尤其在混合部署（本地数据中心 + 云）、统一运维以及 AI 与传统应用混合工作负载等场景下，Kubernetes
依然是理想的控制平面。然而，要避免退居幕后，Kubernetes 必须正视并解决 AI 工作负载带来的特殊挑战，包括：

1. 高级 GPU 调度：提供对 GPU 等加速硬件的感知调度能力，匹配或集成诸如 Run:ai 之类框架的功能。AI 模型训练训练（Training）使用数据集调整模型参数的过程，使模型能够学习数据中的模式。常涉及大量 GPU 任务调度，Kubernetes 需要更智能地分配这些昂贵资源，以提高利用率。
1. 深度 AI 框架集成：与分布式 AI 计算框架深度融合，确保在 Kubernetes 上无缝编排像 Ray、PyTorchPyTorch主流深度学习框架，提供灵活易用的模型开发接口。 等分布式训练/推理作业。这意味着 Kubernetes 应该为这些框架提供原生支持或接口，使其可以借助 Kubernetes 的调度和编排能力，同时满足高速通信和跨节点协同的需求。
1. 优化数据管道处理：支持低延迟、高吞吐的数据管道，方便 AI 工作负载高效地访问海量数据集。模型训练和推理对数据依赖极强，Kubernetes 需要在存储编排、数据本地性、缓存机制等方面提供优化，以减少数据瓶颈。
1. 推理服务弹性扩缩：将模型推理 API 视为一等公民，实现对推理服务的自动扩缩和编排管理。随着越来越多的 AI 模型以服务形式对外提供接口，Kubernetes 需要能够根据流量自动伸缩这些模型推理服务，并处理版本更新、流量灰度发布灰度发布（Canary Release）逐步将新版本发布给部分用户，以验证新版本的稳定性和性能。等需求。
上述这些正是 Kubernetes 在 AI 原生时代必须直面的课题。如果不能在这些方面有所突破，Kubernetes 的地位可能会从战略核心变为背景中的基础设施管道——有用但不再举足轻重。


### Cloud Native 与 AI Native 技术栈的不同

云原生技术栈主要围绕微服务架构、容器化部署和持续交付

##### 持续交付（Continuous Delivery）

保持代码随时可以部署到生产状态的开发实践。

来构建，核心包括容器、Kubernetes 编排、服务网格、CI/CD

##### CI/CD（持续集成/持续部署）

一种通过在应用开发阶段引入自动化来频繁向客户交付应用的方法。

流水线等，重视应用的快速迭代部署、弹性伸缩和可观测性。而 AI 原生技术栈在此基础上向更深层次扩展，侧重于异构算力调度、分布式训练以及高效推理优化等方面。换言之，在云原生的基础设施之上，AI 原生场景引入了许多专门针对 AI 工作负载的组件：包括分布式训练框架（如 PyTorch DDP、TensorFlow MultiWorker）、模型服务化框架（如 KServe、Seldon）、高速数据管道和消息系统（如 Kafka、Pulsar）、新的数据库类型如向量数据库（Milvus、Chroma 等）以及用于追踪模型性能的观测工具等。CNCF 于 2024 年发布的[云原生 AI 白皮书](https://www.cncf.io/reports/cloud-native-artificial-intelligence-whitepaper/)中给出了一张技术景观图，清晰地展示了 AI Native 如何扩展了 Cloud Native 的边界，在原有技术栈上叠加了诸多 AI 特定的工具和框架。

[图 1: 云原生 AI 景观图（根据 CNCF 云原生 AI 白皮书绘制）]

<!-- visual-asset
Asset: (inline svg)
Source: https://assets.jimmysong.io/images/blog/cloud-native-ai-whitepaper/cloud-native-ai.svg
Type: svg
Extracted size: 923x866
Alt text: 图 1: 云原生 AI 景观图（根据 CNCF 云原生 AI 白皮书绘制）
Transcription status: embedded inline as vector SVG; no separate asset file
Multimodal status: vector SVG markup is embedded inline below this note; inspect it directly for visual details.
Text-only fallback: the inline SVG markup carries the diagram's text labels and structure; alt text, source URL, and dimensions are also available.
Mermaid: not inferred automatically; add only after visual inspection confirms a diagram, flowchart, graph, or timeline.
-->

<svg xmlns="http://www.w3.org/2000/svg" xmlns:dc="http://purl.org/dc/elements/1.1/" version="1.1" xmlns:xl="http://www.w3.org/1999/xlink" viewBox="168 295 923 866" width="923" height="866">
  <defs>
    <marker orient="auto" overflow="visible" markerUnits="strokeWidth" id="FilledArrow_Marker" stroke-linejoin="miter" stroke-miterlimit="10" viewBox="-1 -4 10 8" markerWidth="10" markerHeight="8" color="#a5a5a5">
      <g>
        <path d="M 8 0 L 0 -3 L 0 3 Z" fill="currentColor" stroke="currentColor" stroke-width="1"/>
      </g>
    </marker>
  </defs>
  <g id="Canvas_1" stroke-dasharray="none" stroke="none" stroke-opacity="1" fill="none" fill-opacity="1">
    <title>Cloud Native AI</title>
    <rect fill="white" x="168" y="295" width="923" height="866"/>
    <g id="Canvas_1_Layer_1">
      <title>Layer 1</title>
      <g id="Graphic_163"/>
      <g id="Graphic_5">
        <ellipse cx="764.25" cy="402.1702" rx="98.2501569938613" ry="94.0001502027783" fill="#ffff40"/>
        <ellipse cx="764.25" cy="402.1702" rx="98.2501569938613" ry="94.0001502027783" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Graphic_31">
        <path d="M 391.064 546.5 L 891.064 546.5 C 895.4823 546.5 899.064 550.0817 899.064 554.5 L 899.064 625.8523 C 899.064 630.2706 895.4823 633.8523 891.064 633.8523 L 391.064 633.8523 C 386.6457 633.8523 383.064 630.2706 383.064 625.8523 L 383.064 554.5 C 383.064 550.0817 386.6457 546.5 391.064 546.5 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Group_92">
        <g id="Graphic_84">
          <text transform="translate(406.186 1126.9084)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="16.364185" y="13">Intel</tspan>
          </text>
        </g>
        <g id="Graphic_85">
          <text transform="translate(487.4461 1126.9084)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="7.166185" y="13">NVIDIA</tspan>
          </text>
        </g>
        <g id="Graphic_86">
          <text transform="translate(569.2765 1126.9084)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="16.749185" y="13">Arm</tspan>
          </text>
        </g>
        <g id="Graphic_87">
          <text transform="translate(651.1069 1126.9084)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="6.907185" y="13">Google</tspan>
          </text>
        </g>
        <g id="Graphic_88">
          <text transform="translate(731.2265 1126.9084)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="14.026185" y="13">AMD</tspan>
          </text>
        </g>
        <g id="Graphic_89">
          <text transform="translate(814.7676 1125.1044)" fill="black">
            <tspan font-family="PingFang SC" font-size="14" fill="black" x="22.587185" y="15">…</tspan>
          </text>
        </g>
      </g>
      <g id="Graphic_82">
        <path d="M 391.064 1052.7562 L 891.064 1052.7562 C 895.4823 1052.7562 899.064 1056.3379 899.064 1060.7562 L 899.064 1107.7684 C 899.064 1112.1866 895.4823 1115.7684 891.064 1115.7684 L 391.064 1115.7684 C 386.6457 1115.7684 383.064 1112.1866 383.064 1107.7684 L 383.064 1060.7562 C 383.064 1056.3379 386.6457 1052.7562 391.064 1052.7562 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Graphic_51">
        <path d="M 391.064 830.2438 L 891.064 830.2438 C 895.4823 830.2438 899.064 833.8255 899.064 838.2438 L 899.064 885.256 C 899.064 889.6742 895.4823 893.256 891.064 893.256 L 391.064 893.256 C 386.6457 893.256 383.064 889.6742 383.064 885.256 L 383.064 838.2438 C 383.064 833.8255 386.6457 830.2438 391.064 830.2438 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Graphic_26">
        <path d="M 391.064 684.1821 L 891.064 684.1821 C 895.4823 684.1821 899.064 687.7638 899.064 692.1821 L 899.064 739.1943 C 899.064 743.6125 895.4823 747.1943 891.064 747.1943 L 391.064 747.1943 C 386.6457 747.1943 383.064 743.6125 383.064 739.1943 L 383.064 692.1821 C 383.064 687.7638 386.6457 684.1821 391.064 684.1821 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Graphic_2">
        <ellipse cx="571.007" cy="402.1702" rx="147.750236090005" ry="94.0001502027783" fill="#c0ffc0"/>
        <ellipse cx="571.007" cy="402.1702" rx="147.750236090005" ry="94.0001502027783" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Graphic_3">
        <ellipse cx="601.757" cy="402.1702" rx="117.000186954522" ry="64.5001030646723" fill="#80ffff"/>
        <ellipse cx="601.757" cy="402.1702" rx="117.000186954522" ry="64.5001030646723" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Graphic_4">
        <ellipse cx="629.507" cy="402.1702" rx="89.2501426127443" ry="42.0000671118797" fill="#ffffc0"/>
        <ellipse cx="629.507" cy="402.1702" rx="89.2501426127443" ry="42.0000671118797" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Graphic_6">
        <text transform="translate(576.147 387.83422)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="21.444" y="11">Deep</tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="7105427e-20" y="25.336">Learning (DL)</tspan>
        </text>
      </g>
      <g id="Graphic_8">
        <text transform="translate(489.9292 392.84206) rotate(-41)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="13.776" y="11">Machine</tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="48316906e-20" y="25.336">Learning (ML)</tspan>
        </text>
      </g>
      <g id="Graphic_9">
        <text transform="translate(428.30484 381.58586) rotate(-41)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="18.006" y="11">Artificial</tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="0" y="25.336">Inteligence (AI)</tspan>
        </text>
      </g>
      <g id="Graphic_10">
        <text transform="translate(739.257 373.49822)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="1278977e-19" y="11">Math &amp; Statistics</tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x=".57" y="25.336">Exploratory Data</tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="3.57" y="39.671997">Analaysis (EDA)</tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="12.24" y="54.007996">Visualization</tspan>
        </text>
      </g>
      <g id="Group_27">
        <g id="Graphic_19">
          <path d="M 409.186 559.4282 L 621.774 559.4282 C 626.1923 559.4282 629.774 563.0099 629.774 567.4282 L 629.774 610.9241 C 629.774 615.3424 626.1923 618.9241 621.774 618.9241 L 409.186 618.9241 C 404.7677 618.9241 401.186 615.3424 401.186 610.9241 L 401.186 567.4282 C 401.186 563.0099 404.7677 559.4282 409.186 559.4282 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
        </g>
        <g id="Graphic_14">
          <text transform="translate(417.716 568.9282)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="18474111e-20" y="12">Classification</tspan>
          </text>
        </g>
        <g id="Graphic_15">
          <text transform="translate(518.762 568.9282)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="0" y="12">Object Detection</tspan>
          </text>
        </g>
        <g id="Graphic_16">
          <text transform="translate(417.716 594.2763)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="0" y="12">Clustering</tspan>
          </text>
        </g>
        <g id="Graphic_17">
          <text transform="translate(504.186 594.2763)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="9947598e-20" y="12">Forecasting</tspan>
          </text>
        </g>
        <g id="Graphic_18">
          <text transform="translate(587.186 594.2763)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="0" y="12">…</tspan>
          </text>
        </g>
      </g>
      <g id="Group_28">
        <g id="Graphic_25">
          <path d="M 658.354 559.4282 L 870.942 559.4282 C 875.3603 559.4282 878.942 563.0099 878.942 567.4282 L 878.942 610.9241 C 878.942 615.3424 875.3603 618.9241 870.942 618.9241 L 658.354 618.9241 C 653.9357 618.9241 650.354 615.3424 650.354 610.9241 L 650.354 567.4282 C 650.354 563.0099 653.9357 559.4282 658.354 559.4282 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
        </g>
        <g id="Graphic_24">
          <text transform="translate(688.232 568.9282)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="2344791e-19" y="12">RAGs</tspan>
          </text>
        </g>
        <g id="Graphic_23">
          <text transform="translate(757.854 568.9282)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="0" y="12">LLMs</tspan>
          </text>
        </g>
        <g id="Graphic_22">
          <text transform="translate(664.1 594.2763)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="0" y="12">Vector DBs</tspan>
          </text>
        </g>
        <g id="Graphic_21">
          <text transform="translate(771.036 594.2763)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="0" y="12">LVMs</tspan>
          </text>
        </g>
        <g id="Graphic_20">
          <text transform="translate(836.354 594.2763)" fill="black">
            <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="0" y="12">…</tspan>
          </text>
        </g>
      </g>
      <g id="Graphic_29">
        <text transform="translate(483.182 524.0939)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="682121e-18" y="14">Predictive</tspan>
        </text>
      </g>
      <g id="Graphic_30">
        <text transform="translate(729.634 524.0939)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="0" y="14">Generative</tspan>
        </text>
      </g>
      <g id="Graphic_33">
        <path d="M 409.186 696.3522 L 511.622 696.3522 C 516.04027 696.3522 519.622 699.9339 519.622 704.3522 L 519.622 727.0242 C 519.622 731.44245 516.04027 735.0242 511.622 735.0242 L 409.186 735.0242 C 404.7677 735.0242 401.186 731.44245 401.186 727.0242 L 401.186 704.3522 C 401.186 699.9339 404.7677 696.3522 409.186 696.3522 Z" fill="aqua"/>
        <path d="M 409.186 696.3522 L 511.622 696.3522 C 516.04027 696.3522 519.622 699.9339 519.622 704.3522 L 519.622 727.0242 C 519.622 731.44245 516.04027 735.0242 511.622 735.0242 L 409.186 735.0242 C 404.7677 735.0242 401.186 731.44245 401.186 727.0242 L 401.186 704.3522 C 401.186 699.9339 404.7677 696.3522 409.186 696.3522 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(406.186 708.5202)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="8.989999" y="11">Data Preparation</tspan>
        </text>
      </g>
      <g id="Graphic_34">
        <path d="M 549.722 696.3522 L 601.452 696.3522 C 605.8703 696.3522 609.452 699.9339 609.452 704.3522 L 609.452 727.0242 C 609.452 731.44245 605.8703 735.0242 601.452 735.0242 L 549.722 735.0242 C 545.3037 735.0242 541.722 731.44245 541.722 727.0242 L 541.722 704.3522 C 541.722 699.9339 545.3037 696.3522 549.722 696.3522 Z" fill="aqua"/>
        <path d="M 549.722 696.3522 L 601.452 696.3522 C 605.8703 696.3522 609.452 699.9339 609.452 704.3522 L 609.452 727.0242 C 609.452 731.44245 605.8703 735.0242 601.452 735.0242 L 549.722 735.0242 C 545.3037 735.0242 541.722 731.44245 541.722 727.0242 L 541.722 704.3522 C 541.722 699.9339 545.3037 696.3522 549.722 696.3522 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(546.722 701.3522)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="12.083" y="11">Model </tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="7.973" y="25.336">Training</tspan>
        </text>
      </g>
      <g id="Graphic_35">
        <path d="M 639.552 696.3522 L 691.282 696.3522 C 695.7003 696.3522 699.282 699.9339 699.282 704.3522 L 699.282 727.0242 C 699.282 731.44245 695.7003 735.0242 691.282 735.0242 L 639.552 735.0242 C 635.1337 735.0242 631.552 731.44245 631.552 727.0242 L 631.552 704.3522 C 631.552 699.9339 635.1337 696.3522 639.552 696.3522 Z" fill="#ffffc0"/>
        <path d="M 639.552 696.3522 L 691.282 696.3522 C 695.7003 696.3522 699.282 699.9339 699.282 704.3522 L 699.282 727.0242 C 699.282 731.44245 695.7003 735.0242 691.282 735.0242 L 639.552 735.0242 C 635.1337 735.0242 631.552 731.44245 631.552 727.0242 L 631.552 704.3522 C 631.552 699.9339 635.1337 696.3522 639.552 696.3522 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(636.552 701.3522)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="12.083" y="11">Model</tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="8.645" y="25.336">Serving</tspan>
        </text>
      </g>
      <g id="Graphic_36">
        <path d="M 729.382 696.3522 L 781.112 696.3522 C 785.5303 696.3522 789.112 699.9339 789.112 704.3522 L 789.112 727.0242 C 789.112 731.44245 785.5303 735.0242 781.112 735.0242 L 729.382 735.0242 C 724.9637 735.0242 721.382 731.44245 721.382 727.0242 L 721.382 704.3522 C 721.382 699.9339 724.9637 696.3522 729.382 696.3522 Z" fill="#ffffc0"/>
        <path d="M 729.382 696.3522 L 781.112 696.3522 C 785.5303 696.3522 789.112 699.9339 789.112 704.3522 L 789.112 727.0242 C 789.112 731.44245 785.5303 735.0242 781.112 735.0242 L 729.382 735.0242 C 724.9637 735.0242 721.382 731.44245 721.382 727.0242 L 721.382 704.3522 C 721.382 699.9339 724.9637 696.3522 729.382 696.3522 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(726.382 708.5202)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="1.0969998" y="11">Perf/Scale</tspan>
        </text>
      </g>
      <g id="Graphic_37">
        <path d="M 819.212 696.3522 L 870.942 696.3522 C 875.3603 696.3522 878.942 699.9339 878.942 704.3522 L 878.942 727.0242 C 878.942 731.44245 875.3603 735.0242 870.942 735.0242 L 819.212 735.0242 C 814.7937 735.0242 811.212 731.44245 811.212 727.0242 L 811.212 704.3522 C 811.212 699.9339 814.7937 696.3522 819.212 696.3522 Z" fill="#c0ffc0"/>
        <path d="M 819.212 696.3522 L 870.942 696.3522 C 875.3603 696.3522 878.942 699.9339 878.942 704.3522 L 878.942 727.0242 C 878.942 731.44245 875.3603 735.0242 870.942 735.0242 L 819.212 735.0242 C 814.7937 735.0242 811.212 731.44245 811.212 727.0242 L 811.212 704.3522 C 811.212 699.9339 814.7937 696.3522 819.212 696.3522 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(816.212 708.5202)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="6.305" y="11">Observe</tspan>
        </text>
      </g>
      <g id="Graphic_38">
        <text transform="translate(242.277 570.126)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="0" y="14">Workloads</tspan>
        </text>
      </g>
      <g id="Graphic_39">
        <text transform="translate(203 597.5321)" fill="#666">
          <tspan font-family="Helvetica Neue" font-size="14" fill="#666" x="0" y="13">Models, applications,…</tspan>
        </text>
      </g>
      <g id="Graphic_41">
        <text transform="translate(235.788 686.2261)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="58264504e-20" y="14">ML Lifecycle</tspan>
        </text>
      </g>
      <g id="Graphic_40">
        <text transform="translate(223.349 713.6322)" fill="#666">
          <tspan font-family="Helvetica Neue" font-size="14" fill="#666" x="881073e-18" y="13">(AI/ML/LLM Ops)</tspan>
        </text>
      </g>
      <g id="Graphic_42">
        <path d="M 410.57 759 L 466.828 759 C 471.2463 759 474.828 762.5817 474.828 767 L 474.828 789.672 C 474.828 794.0903 471.2463 797.672 466.828 797.672 L 410.57 797.672 C 406.1517 797.672 402.57 794.0903 402.57 789.672 L 402.57 767 C 402.57 762.5817 406.1517 759 410.57 759 Z" fill="aqua"/>
        <path d="M 410.57 759 L 466.828 759 C 471.2463 759 474.828 762.5817 474.828 767 L 474.828 789.672 C 474.828 794.0903 471.2463 797.672 466.828 797.672 L 410.57 797.672 C 406.1517 797.672 402.57 794.0903 402.57 789.672 L 402.57 767 C 402.57 762.5817 406.1517 759 410.57 759 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(407.57 764)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="18.571" y="11">Data </tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x=".12699971" y="25.336">Preparation</tspan>
        </text>
      </g>
      <g id="Graphic_43">
        <path d="M 502.16084 760.0352 L 546.04884 760.0352 C 550.4671 760.0352 554.04884 763.6169 554.04884 768.0352 L 554.04884 790.7072 C 554.04884 795.1254 550.4671 798.7072 546.04884 798.7072 L 502.16084 798.7072 C 497.74256 798.7072 494.16084 795.1254 494.16084 790.7072 L 494.16084 768.0352 C 494.16084 763.6169 497.74256 760.0352 502.16084 760.0352 Z" fill="aqua"/>
        <path d="M 502.16084 760.0352 L 546.04884 760.0352 C 550.4671 760.0352 554.04884 763.6169 554.04884 768.0352 L 554.04884 790.7072 C 554.04884 795.1254 550.4671 798.7072 546.04884 798.7072 L 502.16084 798.7072 C 497.74256 798.7072 494.16084 795.1254 494.16084 790.7072 L 494.16084 768.0352 C 494.16084 763.6169 497.74256 760.0352 502.16084 760.0352 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(499.16084 765.0352)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="4.7179983" y="11">Feature </tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="10.609998" y="25.336">Store</tspan>
        </text>
      </g>
      <g id="Graphic_44">
        <path d="M 581.3817 759.2588 L 653.6533 759.2588 C 658.0716 759.2588 661.6533 762.8405 661.6533 767.2588 L 661.6533 789.9308 C 661.6533 794.3491 658.0716 797.9308 653.6533 797.9308 L 581.3817 797.9308 C 576.9634 797.9308 573.3817 794.3491 573.3817 789.9308 L 573.3817 767.2588 C 573.3817 762.8405 576.9634 759.2588 581.3817 759.2588 Z" fill="aqua"/>
        <path d="M 581.3817 759.2588 L 653.6533 759.2588 C 658.0716 759.2588 661.6533 762.8405 661.6533 767.2588 L 661.6533 789.9308 C 661.6533 794.3491 658.0716 797.9308 653.6533 797.9308 L 581.3817 797.9308 C 576.9634 797.9308 573.3817 794.3491 573.3817 789.9308 L 573.3817 767.2588 C 573.3817 762.8405 576.9634 759.2588 581.3817 759.2588 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(578.3817 764.2588)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="22.353815" y="11">Model</tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="3.5678147" y="25.336">Development</tspan>
        </text>
      </g>
      <g id="Graphic_45">
        <path d="M 688.98616 759.5176 L 725.8742 759.5176 C 730.2924 759.5176 733.8742 763.0993 733.8742 767.5176 L 733.8742 790.1896 C 733.8742 794.6079 730.2924 798.1896 725.8742 798.1896 L 688.98616 798.1896 C 684.5679 798.1896 680.98616 794.6079 680.98616 790.1896 L 680.98616 767.5176 C 680.98616 763.0993 684.5679 759.5176 688.98616 759.5176 Z" fill="aqua"/>
        <path d="M 688.98616 759.5176 L 725.8742 759.5176 C 730.2924 759.5176 733.8742 763.0993 733.8742 767.5176 L 733.8742 790.1896 C 733.8742 794.6079 730.2924 798.1896 725.8742 798.1896 L 688.98616 798.1896 C 684.5679 798.1896 680.98616 794.6079 680.98616 790.1896 L 680.98616 767.5176 C 680.98616 763.0993 684.5679 759.5176 688.98616 759.5176 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(685.98616 764.5176)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="4.662" y="11">Model</tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x=".33600024" y="25.336">Storage</tspan>
        </text>
      </g>
      <g id="Graphic_46">
        <path d="M 761.207 759.7764 L 798.095 759.7764 C 802.5133 759.7764 806.095 763.3581 806.095 767.7764 L 806.095 790.4484 C 806.095 794.8666 802.5133 798.4484 798.095 798.4484 L 761.207 798.4484 C 756.7887 798.4484 753.207 794.8666 753.207 790.4484 L 753.207 767.7764 C 753.207 763.3581 756.7887 759.7764 761.207 759.7764 Z" fill="aqua"/>
        <path d="M 761.207 759.7764 L 798.095 759.7764 C 802.5133 759.7764 806.095 763.3581 806.095 767.7764 L 806.095 790.4484 C 806.095 794.8666 802.5133 798.4484 798.095 798.4484 L 761.207 798.4484 C 756.7887 798.4484 753.207 794.8666 753.207 790.4484 L 753.207 767.7764 C 753.207 763.3581 756.7887 759.7764 761.207 759.7764 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(758.207 764.7764)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="4.662" y="11">Model</tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="1.2240002" y="25.336">Serving</tspan>
        </text>
      </g>
      <g id="Line_47">
        <line x1="474.828" y1="778.7739" x2="484.26157" y2="778.8882" marker-end="url(#FilledArrow_Marker)" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Line_48">
        <line x1="554.04884" y1="779.1223" x2="563.482" y2="779.0439" marker-end="url(#FilledArrow_Marker)" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Line_49">
        <line x1="661.6533" y1="778.7218" x2="671.0862" y2="778.749" marker-end="url(#FilledArrow_Marker)" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Line_50">
        <line x1="733.8742" y1="778.9483" x2="743.3071" y2="778.9821" marker-end="url(#FilledArrow_Marker)" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Graphic_52">
        <path d="M 410.57 842.4139 L 480.828 842.4139 C 485.2463 842.4139 488.828 845.9956 488.828 850.4139 L 488.828 873.0859 C 488.828 877.5042 485.2463 881.0859 480.828 881.0859 L 410.57 881.0859 C 406.1517 881.0859 402.57 877.5042 402.57 873.0859 L 402.57 850.4139 C 402.57 845.9956 406.1517 842.4139 410.57 842.4139 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(407.57 854.5819)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="11.231002" y="11">OpenShift</tspan>
        </text>
      </g>
      <g id="Graphic_53">
        <path d="M 516.5758 842.4139 L 547.6448 842.4139 C 552.0631 842.4139 555.6448 845.9956 555.6448 850.4139 L 555.6448 873.0859 C 555.6448 877.5042 552.0631 881.0859 547.6448 881.0859 L 516.5758 881.0859 C 512.1575 881.0859 508.5758 877.5042 508.5758 873.0859 L 508.5758 850.4139 C 508.5758 845.9956 512.1575 842.4139 516.5758 842.4139 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(513.5758 854.5819)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="6.3125" y="11">GKE</tspan>
        </text>
      </g>
      <g id="Graphic_54">
        <path d="M 583.3926 842.4139 L 653.6506 842.4139 C 658.0689 842.4139 661.6506 845.9956 661.6506 850.4139 L 661.6506 873.0859 C 661.6506 877.5042 658.0689 881.0859 653.6506 881.0859 L 583.3926 881.0859 C 578.9743 881.0859 575.3926 877.5042 575.3926 873.0859 L 575.3926 850.4139 C 575.3926 845.9956 578.9743 842.4139 583.3926 842.4139 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(580.3926 854.5819)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="7.235002" y="11">Kubernetes</tspan>
        </text>
      </g>
      <g id="Graphic_55">
        <path d="M 689.3984 842.4139 L 726.2864 842.4139 C 730.7047 842.4139 734.2864 845.9956 734.2864 850.4139 L 734.2864 873.0859 C 734.2864 877.5042 730.7047 881.0859 726.2864 881.0859 L 689.3984 881.0859 C 684.9801 881.0859 681.3984 877.5042 681.3984 873.0859 L 681.3984 850.4139 C 681.3984 845.9956 684.9801 842.4139 689.3984 842.4139 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(686.3984 854.5819)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="9.666" y="11">AKS</tspan>
        </text>
      </g>
      <g id="Graphic_56">
        <path d="M 762.0342 842.4139 L 798.9222 842.4139 C 803.3405 842.4139 806.9222 845.9956 806.9222 850.4139 L 806.9222 873.0859 C 806.9222 877.5042 803.3405 881.0859 798.9222 881.0859 L 762.0342 881.0859 C 757.6159 881.0859 754.0342 877.5042 754.0342 873.0859 L 754.0342 850.4139 C 754.0342 845.9956 757.6159 842.4139 762.0342 842.4139 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(759.0342 854.5819)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="1.4400002" y="11">Knative</tspan>
        </text>
      </g>
      <g id="Graphic_57">
        <text transform="translate(831.67 852.0178)" fill="black">
          <tspan font-family="Helvetica Neue" font-weight="bold" font-size="16" fill="black" x="13.444" y="16">…</tspan>
        </text>
      </g>
      <g id="Line_58">
        <line x1="555.6448" y1="861.7499" x2="575.3926" y2="861.7499" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_59">
        <line x1="681.3984" y1="861.7499" x2="661.6506" y2="861.7499" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_65">
        <path d="M 484.19845 880.3433 C 497.6045 884.7999 513.78775 888.2979 531.5603 888.2979 C 549.5344 888.2979 566.0312 884.7201 579.71306 880.1913" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_66">
        <path d="M 755.794 878.0924 C 744.0256 883.5629 728.2426 888.2979 708.86525 888.2979 C 691.0452 888.2979 673.4397 884.2934 658.57005 879.395" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Graphic_67">
        <path d="M 391.064 941.5 L 891.064 941.5 C 895.4823 941.5 899.064 945.0817 899.064 949.5 L 899.064 996.5122 C 899.064 1000.9304 895.4823 1004.5122 891.064 1004.5122 L 391.064 1004.5122 C 386.6457 1004.5122 383.064 1000.9304 383.064 996.5122 L 383.064 949.5 C 383.064 945.0817 386.6457 941.5 391.064 941.5 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Graphic_68">
        <path d="M 409.186 953.6701 L 479.444 953.6701 C 483.86227 953.6701 487.444 957.2518 487.444 961.6701 L 487.444 984.3421 C 487.444 988.7604 483.86227 992.3421 479.444 992.3421 L 409.186 992.3421 C 404.7677 992.3421 401.186 988.7604 401.186 984.3421 L 401.186 961.6701 C 401.186 957.2518 404.7677 953.6701 409.186 953.6701 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(406.186 965.8381)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="24.941002" y="11">AWS</tspan>
        </text>
      </g>
      <g id="Graphic_69">
        <path d="M 515.403 953.6701 L 585.661 953.6701 C 590.0793 953.6701 593.661 957.2518 593.661 961.6701 L 593.661 984.3421 C 593.661 988.7604 590.0793 992.3421 585.661 992.3421 L 515.403 992.3421 C 510.9847 992.3421 507.403 988.7604 507.403 984.3421 L 507.403 961.6701 C 507.403 957.2518 510.9847 953.6701 515.403 953.6701 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(512.403 965.8381)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="22.913002" y="11">Azure</tspan>
        </text>
      </g>
      <g id="Graphic_70">
        <path d="M 621.62 953.6701 L 691.878 953.6701 C 696.2963 953.6701 699.878 957.2518 699.878 961.6701 L 699.878 984.3421 C 699.878 988.7604 696.2963 992.3421 691.878 992.3421 L 621.62 992.3421 C 617.2017 992.3421 613.62 988.7604 613.62 984.3421 L 613.62 961.6701 C 613.62 957.2518 617.2017 953.6701 621.62 953.6701 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(618.62 965.8381)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="9.125002" y="11">Bare Metal</tspan>
        </text>
      </g>
      <g id="Graphic_71">
        <path d="M 727.837 953.6701 L 798.095 953.6701 C 802.5133 953.6701 806.095 957.2518 806.095 961.6701 L 806.095 984.3421 C 806.095 988.7604 802.5133 992.3421 798.095 992.3421 L 727.837 992.3421 C 723.4187 992.3421 719.837 988.7604 719.837 984.3421 L 719.837 961.6701 C 719.837 957.2518 723.4187 953.6701 727.837 953.6701 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(724.837 965.8381)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="1.0190016" y="11">Google Cloud</tspan>
        </text>
      </g>
      <g id="Graphic_72">
        <text transform="translate(831.054 963.274)" fill="black">
          <tspan font-family="Helvetica Neue" font-weight="bold" font-size="16" fill="black" x="13.444" y="16">…</tspan>
        </text>
      </g>
      <g id="Graphic_74">
        <text transform="translate(249.284 832.2878)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="0" y="14">Platform</tspan>
        </text>
      </g>
      <g id="Graphic_73">
        <text transform="translate(197.036 859.6939)" fill="#666">
          <tspan font-family="Helvetica Neue" font-size="14" fill="#666" x="0" y="13">Orchestration/Scheduling</tspan>
        </text>
      </g>
      <g id="Graphic_76">
        <text transform="translate(233.331 943.544)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="9094947e-19" y="14">Infrastructure</tspan>
        </text>
      </g>
      <g id="Graphic_75">
        <text transform="translate(219.842 970.9501)" fill="#666">
          <tspan font-family="Helvetica Neue" font-size="14" fill="#666" x="4902745e-19" y="13">Cloud or On-prem</tspan>
        </text>
      </g>
      <g id="Graphic_81">
        <path d="M 409.186 1064.9263 L 477.12774 1064.9263 C 481.546 1064.9263 485.12774 1068.508 485.12774 1072.9263 L 485.12774 1095.5983 C 485.12774 1100.0166 481.546 1103.5983 477.12774 1103.5983 L 409.186 1103.5983 C 404.7677 1103.5983 401.186 1100.0166 401.186 1095.5983 L 401.186 1072.9263 C 401.186 1068.508 404.7677 1064.9263 409.186 1064.9263 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(406.186 1077.0943)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="24.418875" y="11">CPU</tspan>
        </text>
      </g>
      <g id="Graphic_80">
        <path d="M 507.79356 1064.9263 L 575.7353 1064.9263 C 580.1536 1064.9263 583.7353 1068.508 583.7353 1072.9263 L 583.7353 1095.5983 C 583.7353 1100.0166 580.1536 1103.5983 575.7353 1103.5983 L 507.79356 1103.5983 C 503.3753 1103.5983 499.79356 1100.0166 499.79356 1095.5983 L 499.79356 1072.9263 C 499.79356 1068.508 503.3753 1064.9263 507.79356 1064.9263 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(504.79356 1077.0943)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="24.196875" y="11">GPU</tspan>
        </text>
      </g>
      <g id="Graphic_79">
        <path d="M 606.4011 1064.9263 L 674.3429 1064.9263 C 678.76115 1064.9263 682.3429 1068.508 682.3429 1072.9263 L 682.3429 1095.5983 C 682.3429 1100.0166 678.76115 1103.5983 674.3429 1103.5983 L 606.4011 1103.5983 C 601.98285 1103.5983 598.4011 1100.0166 598.4011 1095.5983 L 598.4011 1072.9263 C 598.4011 1068.508 601.98285 1064.9263 606.4011 1064.9263 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(603.4011 1077.0943)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="24.418875" y="11">NPU</tspan>
        </text>
      </g>
      <g id="Graphic_78">
        <path d="M 705.0087 1064.9263 L 772.9504 1064.9263 C 777.3687 1064.9263 780.9504 1068.508 780.9504 1072.9263 L 780.9504 1095.5983 C 780.9504 1100.0166 777.3687 1103.5983 772.9504 1103.5983 L 705.0087 1103.5983 C 700.5904 1103.5983 697.0087 1100.0166 697.0087 1095.5983 L 697.0087 1072.9263 C 697.0087 1068.508 700.5904 1064.9263 705.0087 1064.9263 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(702.0087 1077.0943)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="25.306875" y="11">TPU</tspan>
        </text>
      </g>
      <g id="Graphic_83">
        <path d="M 803.6163 1064.9263 L 871.558 1064.9263 C 875.9763 1064.9263 879.558 1068.508 879.558 1072.9263 L 879.558 1095.5983 C 879.558 1100.0166 875.9763 1103.5983 871.558 1103.5983 L 803.6163 1103.5983 C 799.198 1103.5983 795.6163 1100.0166 795.6163 1095.5983 L 795.6163 1072.9263 C 795.6163 1068.508 799.198 1064.9263 803.6163 1064.9263 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
        <text transform="translate(800.6163 1077.0943)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="24.526875" y="11">DPU</tspan>
        </text>
      </g>
      <g id="Graphic_91">
        <text transform="translate(245.644 1054.8002)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="8171241e-19" y="14">Hardware</tspan>
        </text>
      </g>
      <g id="Graphic_90">
        <text transform="translate(237.503 1082.2063)" fill="#666">
          <tspan font-family="Helvetica Neue" font-size="14" fill="#666" x="43343107e-20" y="13">Accelerators</tspan>
        </text>
      </g>
      <g id="Line_93">
        <line x1="461.81835" y1="1064.9263" x2="531.8705" y2="992.3421" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_94">
        <line x1="484.5238" y1="1069.8714" x2="720.5953" y2="987.7461" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_95">
        <line x1="524.828" y1="1064.9263" x2="461.2514" y2="992.3421" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_96">
        <line x1="543.2882" y1="1064.9263" x2="549.0082" y2="992.3421" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_97">
        <line x1="561.7484" y1="1064.9263" x2="636.765" y2="992.3421" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_98">
        <line x1="743.1483" y1="1064.9263" x2="758.7972" y2="992.3421" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_99">
        <line x1="806.158" y1="1064.9263" x2="688.1781" y2="992.3421" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_100">
        <line x1="444.55553" y1="953.6701" x2="445.45846" y2="881.0859" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_101">
        <line x1="486.9498" y1="958.8957" x2="754.0342" y2="870.5018" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_102">
        <line x1="532.3123" y1="953.6701" x2="463.91866" y2="881.0859" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_103">
        <line x1="577.8721" y1="953.6701" x2="683.7722" y2="878.7733" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_104">
        <line x1="620.2808" y1="953.7817" x2="482.1672" y2="880.9743" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_105">
        <line x1="720.6438" y1="958.1649" x2="488.02124" y2="876.591" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Graphic_107">
        <text transform="translate(502.6598 649.97026)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="0" y="14">CI</tspan>
        </text>
      </g>
      <g id="Graphic_108">
        <text transform="translate(745.139 648.9351)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="17408297e-20" y="14">CD</tspan>
        </text>
      </g>
      <g id="Line_109">
        <line x1="497.8216" y1="672.37636" x2="477.1086" y2="696.3522" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_110">
        <line x1="521.6598" y1="669.0511" x2="553.2285" y2="696.3522" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_111">
        <line x1="740.139" y1="667.40125" x2="694.3777" y2="696.9732" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_112">
        <line x1="755.247" y1="671.3412" x2="755.247" y2="696.3522" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_113">
        <line x1="770.355" y1="667.40125" x2="816.1163" y2="696.9732" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Graphic_114">
        <path d="M 635.564 644.97026 L 646.564 644.97026 L 646.564 664.18626 L 652.064 664.18626 L 641.064 675.18626 L 630.064 664.18626 L 635.564 664.18626 Z" fill="#ccc"/>
        <path d="M 635.564 644.97026 L 646.564 644.97026 L 646.564 664.18626 L 652.064 664.18626 L 641.064 675.18626 L 630.064 664.18626 L 635.564 664.18626 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Graphic_115">
        <path d="M 773.60865 804.6803 L 781.86955 804.6803 L 781.86955 815.3498 L 786 815.3498 L 777.7391 826.3498 L 769.4782 815.3498 L 773.60865 815.3498 Z" fill="#ccc"/>
        <path d="M 773.60865 804.6803 L 781.86955 804.6803 L 781.86955 815.3498 L 786 815.3498 L 777.7391 826.3498 L 769.4782 815.3498 L 773.60865 815.3498 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Graphic_117">
        <title>Account Box</title>
        <path d="M 1011.5 550.5 L 1011.5 578.5 C 1011.5 580.7 1013.28 582.5 1015.5 582.5 L 1043.5 582.5 C 1045.7 582.5 1047.5 580.7 1047.5 578.5 L 1047.5 550.5 C 1047.5 548.3 1045.7 546.5 1043.5 546.5 L 1015.5 546.5 C 1013.28 546.5 1011.5 548.3 1011.5 550.5 Z M 1035.5 558.5 C 1035.5 561.82 1032.82 564.5 1029.5 564.5 C 1026.18 564.5 1023.5 561.82 1023.5 558.5 C 1023.5 555.18 1026.18 552.5 1029.5 552.5 C 1032.82 552.5 1035.5 555.18 1035.5 558.5 Z M 1017.5 574.5 C 1017.5 570.5 1025.5 568.3 1029.5 568.3 C 1033.5 568.3 1041.5 570.5 1041.5 574.5 L 1041.5 576.5 L 1017.5 576.5 L 1017.5 574.5 Z" fill="#666"/>
      </g>
      <g id="Graphic_123">
        <text transform="translate(976.076 584.108)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="7.532" y="13">Data Scientist/ </tspan>
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="18.165" y="29.392">Developers</tspan>
        </text>
      </g>
      <g id="Line_124">
        <line x1="971.076" y1="597.0048" x2="899.064" y2="587.851" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_125">
        <line x1="971.076" y1="601.6514" x2="899.064" y2="711.8301" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_126">
        <line x1="971.076" y1="594.7503" x2="834.6597" y2="467.7302" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Graphic_128">
        <title>Account Box</title>
        <path d="M 1011.5 685.2261 L 1011.5 713.2261 C 1011.5 715.4261 1013.28 717.2261 1015.5 717.2261 L 1043.5 717.2261 C 1045.7 717.2261 1047.5 715.4261 1047.5 713.2261 L 1047.5 685.2261 C 1047.5 683.0261 1045.7 681.2261 1043.5 681.2261 L 1015.5 681.2261 C 1013.28 681.2261 1011.5 683.0261 1011.5 685.2261 Z M 1035.5 693.2261 C 1035.5 696.5461 1032.82 699.2261 1029.5 699.2261 C 1026.18 699.2261 1023.5 696.5461 1023.5 693.2261 C 1023.5 689.9061 1026.18 687.2261 1029.5 687.2261 C 1032.82 687.2261 1035.5 689.9061 1035.5 693.2261 Z M 1017.5 709.2261 C 1017.5 705.2261 1025.5 703.0261 1029.5 703.0261 C 1033.5 703.0261 1041.5 705.2261 1041.5 709.2261 L 1041.5 711.2261 L 1017.5 711.2261 L 1017.5 709.2261 Z" fill="#666"/>
      </g>
      <g id="Graphic_127">
        <text transform="translate(976.076 718.8341)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="17.773" y="13">Data/ML/AI </tspan>
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="25.942" y="29.392">Engineer</tspan>
        </text>
      </g>
      <g id="Line_132">
        <line x1="971.076" y1="727.8778" x2="899.064" y2="619.77134" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_133">
        <line x1="971.076" y1="731.9627" x2="899.064" y2="728.76195" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Graphic_135">
        <title>Account Box</title>
        <path d="M 1011.5 813.0859 L 1011.5 841.0859 C 1011.5 843.2859 1013.28 845.0859 1015.5 845.0859 L 1043.5 845.0859 C 1045.7 845.0859 1047.5 843.2859 1047.5 841.0859 L 1047.5 813.0859 C 1047.5 810.8859 1045.7 809.0859 1043.5 809.0859 L 1015.5 809.0859 C 1013.28 809.0859 1011.5 810.8859 1011.5 813.0859 Z M 1035.5 821.0859 C 1035.5 824.4059 1032.82 827.0859 1029.5 827.0859 C 1026.18 827.0859 1023.5 824.4059 1023.5 821.0859 C 1023.5 817.7659 1026.18 815.0859 1029.5 815.0859 C 1032.82 815.0859 1035.5 817.7659 1035.5 821.0859 Z M 1017.5 837.0859 C 1017.5 833.0859 1025.5 830.8859 1029.5 830.8859 C 1033.5 830.8859 1041.5 833.0859 1041.5 837.0859 L 1041.5 839.0859 L 1017.5 839.0859 L 1017.5 837.0859 Z" fill="#666"/>
      </g>
      <g id="Graphic_134">
        <text transform="translate(976.076 846.6939)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="26.978" y="13">Platform</tspan>
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="25.942" y="29.392">Engineer</tspan>
        </text>
      </g>
      <g id="Graphic_137">
        <title>Account Box</title>
        <path d="M 1011.5 924.3421 L 1011.5 952.3421 C 1011.5 954.5421 1013.28 956.3421 1015.5 956.3421 L 1043.5 956.3421 C 1045.7 956.3421 1047.5 954.5421 1047.5 952.3421 L 1047.5 924.3421 C 1047.5 922.1421 1045.7 920.3421 1043.5 920.3421 L 1015.5 920.3421 C 1013.28 920.3421 1011.5 922.1421 1011.5 924.3421 Z M 1035.5 932.3421 C 1035.5 935.6621 1032.82 938.3421 1029.5 938.3421 C 1026.18 938.3421 1023.5 935.6621 1023.5 932.3421 C 1023.5 929.0221 1026.18 926.3421 1029.5 926.3421 C 1032.82 926.3421 1035.5 929.0221 1035.5 932.3421 Z M 1017.5 948.3421 C 1017.5 944.3421 1025.5 942.1421 1029.5 942.1421 C 1033.5 942.1421 1041.5 944.3421 1041.5 948.3421 L 1041.5 950.3421 L 1017.5 950.3421 L 1017.5 948.3421 Z" fill="#666"/>
      </g>
      <g id="Graphic_136">
        <text transform="translate(976.076 966.1461)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="2.9959998" y="13">SRE/Operations</tspan>
        </text>
      </g>
      <g id="Graphic_139">
        <title>Account Box</title>
        <path d="M 1011.5 1039.6718 L 1011.5 1067.6718 C 1011.5 1069.8718 1013.28 1071.6718 1015.5 1071.6718 L 1043.5 1071.6718 C 1045.7 1071.6718 1047.5 1069.8718 1047.5 1067.6718 L 1047.5 1039.6718 C 1047.5 1037.4718 1045.7 1035.6718 1043.5 1035.6718 L 1015.5 1035.6718 C 1013.28 1035.6718 1011.5 1037.4718 1011.5 1039.6718 Z M 1035.5 1047.6718 C 1035.5 1050.9918 1032.82 1053.6718 1029.5 1053.6718 C 1026.18 1053.6718 1023.5 1050.9918 1023.5 1047.6718 C 1023.5 1044.3518 1026.18 1041.6718 1029.5 1041.6718 C 1032.82 1041.6718 1035.5 1044.3518 1035.5 1047.6718 Z M 1017.5 1063.6718 C 1017.5 1059.6718 1025.5 1057.4718 1029.5 1057.4718 C 1033.5 1057.4718 1041.5 1059.6718 1041.5 1063.6718 L 1041.5 1065.6718 L 1017.5 1065.6718 L 1017.5 1063.6718 Z" fill="#666"/>
      </g>
      <g id="Graphic_138">
        <text transform="translate(976.076 1073.2798)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="23.226" y="13">Hardware</tspan>
          <tspan font-family="Helvetica Neue" font-size="14" fill="black" x="25.55" y="29.392">Architect</tspan>
        </text>
      </g>
      <g id="Line_140">
        <line x1="971.076" y1="855.0404" x2="899.064" y2="729.0279" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_142">
        <line x1="971.076" y1="859.9623" x2="899.064" y2="860.3524" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_143">
        <line x1="971.076" y1="862.8868" x2="895.0673" y2="942.5722" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_144">
        <line x1="971.076" y1="962.1355" x2="899.064" y2="729.2593" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_145">
        <line x1="971.076" y1="971.3065" x2="899.064" y2="973.9574" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_147">
        <line x1="971.076" y1="974.1411" x2="895.0347" y2="1053.8096" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Line_150">
        <line x1="971.076" y1="1086.4479" x2="899.064" y2="1084.2623" stroke="#a5a5a5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4.0,4.0" stroke-width="1"/>
      </g>
      <g id="Graphic_162">
        <path d="M 687.1291 460.3529 C 729.3777 426.3279 729.3777 378.01254 687.1291 343.9875 C 659.0349 378.01254 659.0349 426.3279 687.1291 460.3529 Z" fill="#ffc0ff"/>
        <path d="M 687.1291 460.3529 C 729.3777 426.3279 729.3777 378.01254 687.1291 343.9875 C 659.0349 378.01254 659.0349 426.3279 687.1291 460.3529 Z" stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
      </g>
      <g id="Graphic_7">
        <text transform="translate(671.928 387.83422)" fill="black">
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="8.886" y="11">Data</tspan>
          <tspan font-family="Helvetica Neue" font-size="12" fill="black" x="0" y="25.336">Science</tspan>
        </text>
      </g>
      <g id="Graphic_164">
        <text transform="translate(217.821 399.44407)" fill="black">
          <tspan font-family="Helvetica Neue" font-weight="bold" font-size="16" fill="black" x="0" y="16">Cloud Native AI</tspan>
        </text>
      </g>
    </g>
  </g>
</svg>


图 1: 云原生 AI 景观图（根据 CNCF

##### CNCF（云原生计算基金会）

Cloud Native Computing Foundation，致力于推广云原生技术的非营利组织。

云原生 AI 白皮书绘制）

下面我们按照领域列举云原生/Kubernetes 生态中与 AI 密切相关的一些典型开源项目，来体现 Cloud Native 与 AI Native 技术栈的异同。

#### 通用调度与编排（General Orchestration）

Kubernetes 本身依然是底座，但为更好地支持 AI 任务，出现了诸多在 Kubernetes 之上增强调度能力的项目。例如，Volcano
提供面向批处理和机器学习作业的调度优化，支持任务依赖和公平调度；KubeRay 则通过 Kubernetes 原生控制器来部署和管理 Ray 集群，使大规模分布式计算框架 Ray 可以在
Kubernetes 上弹性伸缩

##### 弹性伸缩（Elastic Scaling）

根据负载自动调整资源的能力，包括水平和垂直伸缩。

。这些工具强化了 Kubernetes 对 AI 工作负载（尤其是需要占用大量 GPU 的任务）的调度治理能力。

#### 分布式训练（Distributed Training）

针对大规模模型的分布式训练，社区也提供了成熟的解决方案。Kubeflow 的 Training Operator

##### Operator（运算器）

用于封装和管理 Kubernetes 应用运维知识的控制器，实现应用的自动化部署和运维。

就是典型代表，它为 Kubernetes 提供自定义资源来定义训练作业（如 TensorFlow Job、PyTorch Job），自动创建相应的 Master/Worker
容器以在集群中并行训练模型。此外，像 Horovod、DeepSpeed、Megatron 等分布式训练框架也能在 Kubernetes 环境下运行，通过 Kubernetes
来管理跨节点的训练进程和资源配置，以实现线性扩展的模型训练能力。

#### 模型服务化（ML Serving）

在模型训练完成后，如何将模型部署为在线服务也是 AI Native 技术栈的重要组成部分。在 Kubernetes 生态中，KServe（前身为 KFServing）和 Seldon Core
是两大常用的模型服务框架，提供了将训练后的模型打包成容器并部署为可自动扩缩的服务的能力。它们支持流量路由、滚动升级和多模型管理，方便地在 Kubernetes 上实现 AB 测试和 Canary
发布等。近年兴起的 vLLM 则是专注于大语言模型（LLM

##### LLM（大语言模型）

一种能够理解和生成人类语言的深度学习算法。

）高性能推理的开源引擎，采用高效的键值缓存架构以提升吞吐，并支持在 Kubernetes 集群上横向扩展部署。例如，vLLM 项目已经从单机版发展出面向集群的“vLLM
production-stack”方案，可以在多 GPU 节点上无缝运行，通过共享缓存和智能路由实现比传统推理服务高数量级的性能提升。

#### 机器学习管道与 CI/CD

在模型从开发到部署的生命周期中，涉及数据准备、特征工程、模型训练、模型评估到上线部署的一系列步骤。Kubeflow Pipelines 等工具在 Kubernetes
上提供了端到端的机器学习工作流编排机制，允许将上述步骤定义为流水线并运行在容器之中，实现一键式的训练到部署流程。同时，诸如 MLflow
等工具与这些流水线集成，用于追踪实验指标、管理模型版本和注册模型，结合 BentoML 等模型打包工具，可以方便地将模型以一致的方式打包部署到 Kubernetes 集群。

#### 数据科学交互环境（Data Science Environments）

数据科学家常用的 Jupyter Notebook 等交互式开发环境也可以通过 Kubernetes 来提供。像 Kubeflow Notebooks 或 JupyterHub on
Kubernetes 让每位用户在集群中获得独立的容器化开发环境，既方便调用大规模数据集和 GPU 资源，又保证不同用户/团队的隔离。这实质上将云原生的多租户能力应用到数据科学场景，使 AI
研发能够在共享的基础设施上进行而不彼此干扰。

#### 工作负载可观测性（Workload Observability）

在 AI 场景下，系统监控和性能追踪同样不可或缺。云原生领域成熟的监控工具如 Prometheus

##### Prometheus

开源监控告警系统，采用拉取模型采集时序数据。

和 Grafana 仍然大显身手，可以收集 GPU 利用率、模型响应延迟等指标，为 AI 工作负载提供监控报警。同时，OpenTelemetry
等开放标准为分布式跟踪提供了基础，使跨服务的调用链路分析也适用于模型推理请求的诊断。另外，Weights &
Biases（W&B）等机器学习实验跟踪平台在模型训练阶段广泛应用，用于记录模型指标、超参数和评估结果。而面对大语言模型的新挑战，一些新兴工具（如 Langfuse、OpenLLMetry
等）开始专注于模型层面的观测，提供对生成内容质量、模型行为的监控手段。这些工具与 Kubernetes 的集成，使运维团队能够像监控传统微服务那样监控 AI 模型的表现。

#### 自动机器学习（AutoML）

为提高模型开发效率，许多团队会使用超参数调优和自动机器学习工具来自动搜索模型的最佳配置。Kubeflow Katib 是一个 Kubernetes 原生的 AutoML
工具，它通过在集群中并行运行大量实验（每个实验跑一个模型训练作业）来试验不同的超参数组合，最终找到最优解。Katib 将每个实验封装为 Kubernetes Pod 并由 Kubernetes
调度，从而充分利用集群空闲资源。类似的还有微软的 NNI (Neural Network

##### Neural Network（神经网络）

受到生物神经网络启发的计算模型。

Intelligence) 等，也支持在 Kubernetes 上运行实验以进行自动调参和模型结构搜索。

#### 数据架构与向量数据库（Data Architecture & Vector Databases）

AI 应用对数据的需求促使传统的大数据技术与云原生结合得更加紧密。一方面，像 Apache Spark、Flink 这类批处理和流处理引擎已经可以在 Kubernetes 上运行，通过
Kubernetes 来管理它们的分布式执行和资源分配。同时，Kafka 和 Pulsar 等消息队列、HDFS、Alluxio 等分布式存储也都可以以 Operator 形式部署在
Kubernetes 集群中，为 AI 工作负载提供弹性的数据管道和存储服务。另一方面，新兴的向量数据库（如 Milvus、Chroma、Weaviate 等）成为 AI
技术栈中特有的组件，用于存储和检索向量化

##### 向量化（Vectorization）

将数据转换为向量表示的过程，用于机器学习和信息检索。

的特征表示，在实现相似度搜索、语义检索等功能时不可或缺。这些向量数据库同样能够部署在 Kubernetes 上运行，有些还提供 Operator 来简化部署管理。通过 Kubernetes
来托管这些数据基础设施，团队可以在同一套集群上同时管理计算（模型推理/训练）和数据服务，实现计算与数据的一体化调度。

#### Service Mesh 与 AI Gateway

在 AI Native 场景中，服务网格不仅仅是传统的东西南北流量治理工具，还逐渐演化为 AI 流量网关。例如：

- Istio / Envoy：通过 Filter 扩展机制支持 AI 流量治理，Envoy 甚至出现了 AI Gateway 原型（[Envoy AI Gateway](https://aigateway.envoyproxy.io/)），能够为推理流量提供统一入口、流量路由和安全策略。
- kgateway：基于 Envoy proxy 的网关，支持 PromptPrompt（提示词）输入给 AI 模型的指令或文本。 Guard 提示词防护、推理服务编排、多模型调度与故障转移。
- kagent：Kubernetes 原生的 Agentic AIAgentic AI（智能体式 AI）具备自主规划、行动与工具调用能力的 AI 形态。 框架，通过 CRD 声明式管理 AI Agent，结合 MCP 协议实现多智能体协作，用于智能诊断和自动化运维。
- agentgateway：专为 AI AgentAI Agent（智能体）一个能够感知环境并采取行动以实现目标的智能体。 通信设计的新型代理（已捐赠给 Linux Foundation），支持 A2A（Agent-to-Agent）通信和 MCP 协议，具备安全治理、可观测性、跨团队工具共享等功能。
- kmcp：面向 MCPMCP（模型上下文协议）用于在模型与外部工具或数据源之间传递上下文的协议标准，定义交互与数据格式。 Server 开发与运维的工具集，提供从 init、build、deploy 到 CRD 控制的全生命周期支持，简化 AI 工具的原生化运行和治理。
这些项目的出现表明，Service Mesh 技术正从 “微服务的流量治理” 扩展为 “AI 应用的智能流量与 Agent


##### Agent（智能体）

能够感知环境并执行动作以达成目标的实体或软件组件。

协作底座”。在 AI Native 架构中，服务网关 + 网格化治理将成为连接 LLM、Agent 与传统微服务的重要桥梁。

通过以上概览可以看出，Cloud Native 生态正在快速扩展以拥抱 AI 场景，各类开源项目让 Kubernetes 成为了承载 AI 工作负载的平台底座。Kubernetes
社区和周边生态正积极将云原生领域的成熟经验（如可扩展的控制平面、声明式 API 管理等）应用到 AI 领域，从而在 Cloud Native 与 AI Native 之间架起桥梁。这种融合既帮助 AI
基础设施继承了云原生的优良基因（弹性、可移植、标准化），也让 Kubernetes 通过扩展和集成保持在 AI 浪潮中的生命力。

### 易用性与未来展望

需要注意的是，Kubernetes 本身的易用性和抽象层次也在受到新的审视。随着 Kubernetes 成为“底座”，开发者希望与之交互的方式变得更简单高效。社区中不乏关于“[Kubernetes 2.0](https://aws.plainenglish.io/kubernetes-2-0-just-killed-yaml-heres-what-google-s-sres-are-really-using-2025-b99960fa614c)”的探讨，有观点认为当前繁琐的 YAML 配置已经成为生产实践中的痛点：据报道称多达 79% 的 Kubernetes 生产故障可追溯到 YAML 配置错误（例如缩进、冒号错漏等）。“YAML 疲劳”引发了对更高级别、更智能的操作界面的呼声，一些人畅想未来的 Kubernetes 将弱化对手工编写 YAML 的依赖，转而采用更自动化、声明意图更简洁的方式来部署应用。例如，有传闻中的“Kubernetes 2.0”雏形展示了不再需要 Helm Chart

##### Helm Chart

用于定义、安装和升级 Kubernetes 应用的一组模板与配置包。

和成百上千行 YAML，仅用一条类似 k8s2 deploy --predict-traffic=5m 的指令即可完成部署的设想。尽管这些还停留在设想或早期尝试阶段，但折射出业界对
Kubernetes 易用性的期待：即在保证强大灵活的同时，尽量降低认知和操作负担。这对于支持复杂的 AI 工作负载尤为重要，因为用户更关心模型本身的迭代，而不希望被底层繁琐的配置细节绊住手脚。

### 技术的“消失”与新机遇

最后，正如 Kubernetes 项目主席（名誉）Kelsey Hightower 所言，如果基础设施的演进符合预期，那么 Kubernetes 终将“消失”在前台，变成像今天的 Linux
一样稳定而无处不在的底层支撑。这并不是说 Kubernetes 会被弃用，而是说当 Kubernetes
足够成熟并被更高层的抽象所封装后，开发者无需感知其中细节，但它依然默默地提供核心能力。这种“淡出视野”恰恰意味着技术的进一步进化。面对 AI 原生时代，Kubernetes
也许不会以原来的样子出现于每个开发者面前，但它很可能以内嵌于各种 AI 平台和工具的形式继续发挥作用——从云到边缘，无处不在地提供统一的资源调度与运行时支持。Kubernetes
一方面需要保持内核的稳定与通用性，另一方面也应该鼓励在其之上构建面向特定领域的上层平台，就如同早期云原生生态中出现的 Heroku、Cloud Foundry 那样，在 Kubernetes
之上为不同场景提供更简化的用户体验。

综上所述，Kubernetes 在 AI Native 时代既面临挑战又充满机遇。只要社区能够顺应潮流，不断演进 Kubernetes 的能力边界并改进易用性，我们有理由相信 Kubernetes
会成为 AI 时代混合计算基础设施的核心支柱，继续在新的十年里发挥不可替代的作用。

### Cloud Native 开源 vs. AI Native 开源

在 Cloud Native 时代，Kubernetes
等基础设施工具的开源不仅意味着源代码开放，更意味着开发者可以在本地完整编译、重构、定制和运行这些工具。社区拥有高度的可控性和创新空间，任何人都能基于开源项目进行深度二次开发，推动生态繁荣。

而在 AI Native 时代，虽然许多大模型

##### 大模型（Large Language Model）

参数规模巨大的深度学习模型，通常指具有数十亿到数万亿参数的语言模型。

（如 Llama、Qwen 等）以“开源”名义发布，甚至开放了模型权重和部分代码，但实际可重构性和可复现性远低于 Cloud Native 工具。主要原因包括：

1. 数据不可得与复现门槛高：根据 OSIOSI（开源促进会）维护开源定义与许可标准的组织。（Open Source Initiative）最新定义，真正的开源 AI 模型不仅要开放权重和代码，还需详细描述训练数据集。但现实中，绝大多数大模型的训练数据无法公开，开发者难以复现原始模型。
1. 工具链复杂且资源门槛高：AI 模型的训练依赖庞大的算力、复杂的数据管道和专有工具链，普通开发者即使获得全部代码和权重，也难以在本地重构或修改模型。
1. 法律与治理障碍：数据版权、隐私保护等法律问题使得开源 AI 的数据流通受限，模型的“开源”更多停留在权重和 API 层面，缺乏 Cloud Native 那样的完整开放。
1. 生态协作模式不同：Cloud Native 项目强调社区驱动、标准化和可插拔架构，而 AI Native 开源更多依赖企业主导和“部分开放”，社区参与度和创新空间有限。
这种差异导致 AI Native 时代的“开源”更多是一种有限开放：开发者可以使用和微调模型，但很难像重构 Kubernetes 那样深度定制和创新。真正的开源 AI
仍在探索阶段，未来需要解决数据开放、工具链标准化和法律治理等多重挑战，才能实现 Cloud Native 式的开放协作。


### AI 领域的开源基金会现状与挑战

在云原生领域，CNCF（Cloud Native Computing Foundation）等基金会通过统一治理、项目孵化和社区协作，极大推动了 Kubernetes 及相关生态的繁荣。然而，AI
领域至今尚未出现类似 CNCF 的统一开源基金会来统筹 AI 基础设施和生态发展。究其原因，主要有以下几点：

1. 技术分散与生态碎片化：AI 技术栈高度分散，涵盖模型、框架、数据、硬件、工具链等多个层面，不同领域（如深度学习、推理、数据管道、Agent 框架等）各自为政，难以像云原生那样形成统一的标准和治理模式。
1. 商业利益与专有壁垒：主流 AI 技术（如大模型、推理 API、Agent 平台）往往由大型科技公司主导，开源项目与商业闭源产品高度交织，企业间缺乏足够的动力推动“中立基金会”统一治理。
1. 治理模式尚未成熟：Linux Foundation 虽然设有 LF AI & Data、PyTorch Foundation 等子基金会，但它们多聚焦于特定项目或领域，缺乏 CNCF 那样的“技术景观图”和统一孵化机制。AI 领域的快速演进和多样化需求，使得基金会难以制定通用的治理框架。
1. 行业观点分歧：如 Linux Foundation CEO [Jim Zemlin 所言](https://thenewstack.io/the-linux-foundation-in-the-age-of-ai/)，AI 领域的开源治理尚处于探索阶段，基金会更倾向于支持具体项目而非打造统一大伞。部分业界人士认为，AI 的创新速度和商业化压力远高于云原生，基金会模式需要新的适应和演化。
目前，AI 领域的开源基金会主要以“项目孵化 + 社区支持”为主，例如 LF AI & Data 支持 ONNX、PyTorch、Milvus 等项目，但尚未形成 CNCF
式的统一技术景观和治理体系。未来，随着 AI 技术标准化和生态成熟，或许会出现类似 CNCF 的统一基金会，但短期内仍以分散治理和多元协作为主。


这一现状也反映在 Kubernetes 与 AI 的融合路径上：Kubernetes 作为云原生的底座，依赖 CNCF 的治理和生态推动，而 AI 领域则更多依靠各自项目和社区的自发协作。只有当 AI
技术栈趋于标准化、行业需求趋同，才有可能诞生类似 CNCF 的统一基金会，推动 AI 基础设施的开放创新。

Kubernetes 在 AI Native 时代正从云原生的“明星”转型为 AI 应用背后的基础平台。面对异构算力、海量数据和智能运维等新需求，Kubernetes 需主动与 AI
生态深度融合，通过插件扩展和框架集成，成为统一承载传统应用与 AI 系统的混合算力底座。无论在混合云还是企业数据中心，Kubernetes 依然是 AI
工作负载不可或缺的核心基础设施，只要持续演进，其在 AI 时代的关键地位将得以巩固。

### 参考资料

- [Kubernetes and beyond: a year-end reflection with Kelsey Hightower - cncf.io](https://www.cncf.io/blog/2024/01/22/kubernetes-and-beyond-a-year-end-reflection-with-kelsey-hightower)
- [Cloud Native Artificial Intelligence Whitepaper – cncf.io](https://www.cncf.io/reports/cloud-native-artificial-intelligence-whitepaper/)
- [Kubernetes in an AI-Native World: Can It Stay Relevant? - clouddon.ai](https://clouddon.ai/kubernetes-in-an-ai-native-world-can-it-stay-relevant-a23a06b26397)
- [Kubernetes 2.0 Might Kill YAML — Here’s the Private Beta That Changed Everything (2025) - aws.plainenglish.io](https://aws.plainenglish.io/kubernetes-2-0-just-killed-yaml-heres-what-google-s-sres-are-really-using-2025-b99960fa614c)
- [The Linux Foundation in the Age of AI - thenewstack.io](https://thenewstack.io/the-linux-foundation-in-the-age-of-ai/)
- [What Is Open Source AI Anyway? - thenewstack.io](https://thenewstack.io/what-is-open-source-ai-anyway/)
![宋净超（Jimmy Song）](20260725-kubernetes-ai-native-jimmy-song_assets/jimmysong-974a4d6f464e.svg)

<!-- visual-asset
Asset: 20260725-kubernetes-ai-native-jimmy-song_assets/jimmysong-974a4d6f464e.svg
Source: https://jimmysong.io/images/jimmysong.jpg
Type: image/jpeg wrapped in svg
Extracted size: 600x600; 42488 bytes
Alt text: 宋净超（Jimmy Song）
Transcription status: preserved as local SVG asset
Multimodal status: local SVG asset is available when Asset is a relative path; inspect it directly for visual details.
Text-only fallback: use alt text, source URL, dimensions, nearby page text, and any explicit caption; visual content is not fully transcribed unless Mermaid or a human/agent note is added.
Mermaid: not inferred automatically; add only after visual inspection confirms a diagram, flowchart, graph, or timeline.
-->


#### 宋净超（Jimmy Song）

专注于 AI 原生基础设施与云原生应用架构的研究与开源实践。

更新于 2025/09/05

[Kubernetes](https://jimmysong.io/zh/tags/kubernetes)
[AI](https://jimmysong.io/zh/tags/ai)
[AI Agent](https://jimmysong.io/zh/tags/ai-agent)
[Cloud Native](https://jimmysong.io/zh/tags/cloud-native)

##### 微信分享

使用微信扫描二维码分享

文章导航

[上一篇](https://jimmysong.io/zh/blog/e2b-browserbase-report/)
[云端智能体基础设施新纪元：E2B 与 Browserbase 深度调研与全球趋势分析](https://jimmysong.io/zh/blog/e2b-browserbase-report/)

[下一篇](https://jimmysong.io/zh/blog/vibe-coding-tools-comparison/)

[氛围编程工具全景对比：从插件到 IDE、从终端到 Agent](https://jimmysong.io/zh/blog/vibe-coding-tools-comparison/)

延伸阅读

#### [Kubernetes AI 应用基础设施开源实践与创新：Solo.io 开源项目研究](https://jimmysong.io/zh/blog/kubernetes-ai-oss-solo/)

[2025-09-01](https://jimmysong.io/zh/blog/kubernetes-ai-oss-solo/)

[云原生](https://jimmysong.io/zh/blog/kubernetes-ai-oss-solo/)

[24min](https://jimmysong.io/zh/blog/kubernetes-ai-oss-solo/)

#### [什么样的 AI 平台算得上 Kubernetes 原生？](https://jimmysong.io/zh/blog/k8s-ai-conformance/)

[2025-11-12](https://jimmysong.io/zh/blog/k8s-ai-conformance/)

[云原生](https://jimmysong.io/zh/blog/k8s-ai-conformance/)

[4min](https://jimmysong.io/zh/blog/k8s-ai-conformance/)

#### [Kubernetes 在 AI 浪潮下的“焦虑”与新生](https://jimmysong.io/zh/blog/kubernetes-in-ai-wave-anxiety-and-rebirth/)

[2026-04-03](https://jimmysong.io/zh/blog/kubernetes-in-ai-wave-anxiety-and-rebirth/)

[云原生](https://jimmysong.io/zh/blog/kubernetes-in-ai-wave-anxiety-and-rebirth/)

[6min](https://jimmysong.io/zh/blog/kubernetes-in-ai-wave-anxiety-and-rebirth/)

评论区
