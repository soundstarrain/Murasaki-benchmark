<div align="center">

<h1>Murasaki Benchmark</h1>

<p>
  <strong>大语言模型日语→中文 ACGN 翻译质量评测基准</strong>
</p>

<p>
  <a href="https://github.com/soundstarrain/murasaki-benchmark/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License">
  </a>
  <img src="https://img.shields.io/badge/Python-3.10+-green" alt="Python">
  <img src="https://img.shields.io/badge/Models-31-orange" alt="Models">
  <img src="https://img.shields.io/badge/Domain-ACGN-pink" alt="Domain">
</p>

<p>
  <a href="#-排行榜">📊 排行榜</a> •
  <a href="#-方法论">🛠️ 方法论</a> •
  <a href="#-快速开始">🚀 快速开始</a> •
  <a href="#-引用">📝 引用</a>
</p>

<br>

<img src="results/murasaki_benchmark_chart.png" alt="评测结果" width="800">

</div>

<br>

> **Murasaki Benchmark** 提供两个段落级数据集（Short/Long），用于评测 LLM 翻译与专业人工译文在 **ACGN 领域**的对齐程度。通过 COMET 指标，我们在段落层面衡量机器翻译与权威参考译文之间的语义相似度。

---

## 排行榜

我们使用 COMET 指标评测了**主流商业模型和开源模型**的日中 ACGN 翻译能力。

| 排名 | 模型 | 短文本 | 长文本 | 平均 |
|:----:|:-----|:------:|:------:|:----:|
| 🥇 | **Gemini 3 Flash Preview** | 0.826 | 0.876 | **0.851** |
| 🥈 | **Sakura-Qwen-2.5-14B** | 0.828 | 0.874 | **0.851** |
| 🥉 | **GPT-5-chat-latest** | 0.825 | 0.876 | **0.851** |
| 4 | Gemini 2.5 Flash | 0.824 | 0.877 | 0.851 |
| 5 | GPT-4.1 | 0.826 | 0.873 | 0.849 |
| 6 | Gemini 3 Pro Preview | 0.824 | 0.875 | 0.849 |
| 7 | Claude Opus 4.5 | 0.824 | 0.873 | 0.849 |
| 8 | Claude Haiku 4.5 | 0.824 | 0.869 | 0.847 |
| 9 | Claude Haiku 4.5 Thinking | 0.825 | 0.865 | 0.845 |
| 10 | DeepSeek V3.2 Thinking | 0.818 | 0.870 | 0.844 |
| 11 | Claude Sonnet 4.5 | 0.815 | 0.868 | 0.842 |
| 12 | Qwen3-14B | 0.812 | 0.870 | 0.841 |
| 13 | GLM-4.7 | 0.810 | 0.866 | 0.838 |
| 14 | o3-mini | 0.811 | 0.866 | 0.838 |
| 15 | o3 | 0.811 | 0.863 | 0.837 |
| 16 | DeepSeek V3.1 Think | 0.812 | 0.862 | 0.837 |
| 17 | GPT-5-mini | 0.812 | 0.861 | 0.836 |
| 18 | Qwen3-235B-A22B | 0.823 | 0.848 | 0.836 |
| 19 | Qwen3-32B | 0.819 | 0.846 | 0.832 |
| 20 | Dolphin3.0-R1-Mistral-24B | 0.806 | 0.858 | 0.832 |
| 21 | Llama-3.1-70B | 0.809 | 0.852 | 0.831 |
| 22 | DeepSeek V3.2 | 0.810 | 0.851 | 0.830 |
| 23 | Mistral Large | 0.803 | 0.856 | 0.830 |
| 24 | Gemini 2.0 Flash | 0.814 | 0.843 | 0.829 |
| 25 | Llama-3.1-405B | 0.801 | 0.851 | 0.826 |
| 26 | Kimi-K2 | 0.778 | 0.841 | 0.810 |
| 27 | DeepSeek V3.1 | 0.795 | 0.824 | 0.809 |
| 28 | Qwen3-8B | 0.760 | 0.839 | 0.799 |
| 29 | Grok-4.1-fast | 0.765 | 0.789 | 0.777 |
| 30 | Grok-4.1 | 0.766 | 0.776 | 0.771 |
| 31 | Llama-3-8B | 0.710 | 0.752 | 0.731 |

完整结果: [results/final_comet_scores.jsonl](results/final_comet_scores.jsonl)

---

## 核心特点

* **段落级评测** — 两个数据集（Short: 180-200字符，Long: 780-800字符）用于全面评估段落翻译能力。
* **权威参考译文** — 来自老牌汉化组和官方台版的专业人工翻译。
* **COMET 评分** — 使用神经网络评估方法衡量 LLM 输出与参考译文的语义对齐程度。
* **公平对比** — 统一 `temperature=1.0` 和标准化 prompt，确保结果可复现、可比较。

---

## 🛠️ 方法论

### 数据构建流程

```mermaid
graph LR
    A[官方 EPUB 日文] --> C{对齐}
    B[汉化组/官方译文 中文] --> C
    C -- Full Matrix DP + BGE-M3 --> D[高置信度过滤]
    D --> E[分层抽样]
    E --> F((Murasaki 数据集))
    
    style F fill:#f9f,stroke:#333,stroke-width:2px
```

### 数据集构成

| 类别 | 样本数 | 长度 (字符) | 内容类型 |
|------|:------:|:-----------:|----------|
| **Short** | 100 | 180-200 | 对话、吐槽、短描写 |
| **Long** | 100 | 780-800 | 复杂世界观、情感独白 |

覆盖商业轻小说及「成为小说家吧」网文的主流题材：

<details>
<summary><strong>点击查看题材覆盖</strong></summary>

| 题材 | 代表作品 |
|------|----------|
| **异世界** | 无职转生、转生史莱姆、盾之勇者 |
| **恋爱喜剧** | 春物、俺妹、辉夜大小姐 |
| **奇幻** | 刀剑神域、为美好世界献上祝福、狼与香辛料 |
| **科幻** | 86不存在的战区、全金属狂潮 |
| **日常** | 邻家天使、义妹生活 |
| **悬疑** | 古典部系列、化物语 |
| **战记** | 幼女战记、银河英雄传说 |

</details>

### 评测协议

| 参数 | 值 |
|------|----|
| Temperature | 1.0 |
| System Prompt | 标准化 ([pipeline/config.py](pipeline/config.py)) |
| 特殊情况 | Sakura 模型使用官方推荐设置 |
| 指标 | COMET (Unbabel/XCOMET-XL) |

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/soundstarrain/murasaki-benchmark
cd murasaki-benchmark
pip install -r requirements.txt
```

### 运行评测

**方式一：本地模型（如通过 Ollama 部署 Qwen）**
```bash
ollama pull qwen2.5:14b
python examples/local_llm_demo.py
```

**方式二：API 调用**
```bash
cp .env.example .env
# 编辑 .env 填写 API 密钥
python examples/api_eval_demo.py
```

> 详细配置请参考 [docs/local_deployment.md](docs/local_deployment.md)

---

## 📂 项目结构

```text
murasaki-benchmark/
├── 📂 data/           # 评测数据集 (Short/Long)
├── 📂 pipeline/       # 核心评测逻辑 (Prompt, 评分)
├── 📂 examples/       # 最小可运行示例
├── 📂 results/        # 完整评测日志和图表
└── 📂 docs/           # 详细文档
```

---

## 📝 引用

如果本基准对您的研究有帮助，请引用：

```bibtex
@misc{murasaki2026,
  title={Murasaki Benchmark: An ACGN Translation Benchmark for LLMs},
  author={Murasaki Team},
  year={2026},
  url={https://github.com/soundstarrain/murasaki-benchmark}
}
```

---

## 📄 许可证

本项目采用 [GPL-3.0](LICENSE) 开源协议。

> 数据集仅供**学术研究**使用。原作小说和译文的版权归原作者所有。
