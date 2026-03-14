<div align="center">

<h1>Murasaki Benchmark</h1>

<p>
  <strong>A Comprehensive Benchmark for Evaluating Japanese-to-Chinese ACGN Translation Quality</strong>
</p>

<p>
  <a href="https://github.com/your-repo/murasaki-benchmark/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License">
  </a>
  <img src="https://img.shields.io/badge/Python-3.10+-green" alt="Python">
  <img src="https://img.shields.io/badge/Models-36-orange" alt="Models">
  <img src="https://img.shields.io/badge/Domain-ACGN-pink" alt="Domain">
</p>

<p>
  <a href="#-leaderboard">📊 Leaderboard</a> •
  <a href="#-methodology">🛠️ Methodology</a> •
  <a href="#-quick-start">🚀 Quick Start</a> •
  <a href="#-citation">📝 Citation</a>
</p>

<br>

<img src="results/murasaki_benchmark_chart.png" alt="Benchmark Results" width="800">

</div>

<br>

> **Murasaki Benchmark** provides two paragraph-level datasets (Short/Long) to evaluate how well LLM translations align with professional human references in the **ACGN domain**. Using COMET (wmt22-comet-da) metric, we measure the semantic similarity between machine translations and authoritative reference translations at the paragraph level.

---

## Leaderboard

We evaluated **SOTA commercial and mainstream open-source LLMs** using the COMET (wmt22-comet-da) metric.

### Long Text Leaderboard (Primary)

> **Note**: Murasaki entries below only keep the `IQ4_XS`, `t=0.3` results; the Sakura result is `IQ4_XS`, `t=0.1`.

| Rank | Model | Long Score |
|:----:|:------|:----------:|
| 🥇 | **murasaki-8b-v0.2 (IQ4_XS, t=0.3)** | **0.8802** |
| 🥈 | **murasaki-14b-v0.2 (IQ4_XS, t=0.3)** | **0.8798** |
| 🥉 | **murasaki-4b-v0.2-think (IQ4_XS, t=0.3)** | **0.8784** |
| 4 | murasaki-4b-v0.2-nonthink (IQ4_XS, t=0.3) | 0.8779 |
| 5 | gemini-2.5-flash | 0.8767 |
| 6 | gemini-3-flash-preview | 0.8765 |
| 7 | gpt-5-chat-latest | 0.8765 |
| 8 | gemini-3-pro-preview | 0.8744 |
| 9 | deepseek-v3.2 | 0.8738 |
| 10 | Sakura-qwen-2.5-14B (IQ4_XS, t=0.1) | 0.8735 |
| 11 | claude-opus-4-5-20251101 | 0.8732 |
| 12 | gpt-4.1 | 0.8724 |
| 13 | deepseek-v3.1 | 0.8714 |
| 14 | qwen3-14b | 0.8702 |
| 15 | deepseek-v3.2-thinking | 0.8701 |
| 16 | qwen3-32b | 0.8699 |
| 17 | qwen3-8b | 0.8698 |
| 18 | translategemma-12b | 0.8688 |
| 19 | claude-haiku-4-5-20251001 | 0.8688 |
| 20 | gemini-2.0-flash | 0.8688 |
| 21 | claude-sonnet-4-5-20250929 | 0.8682 |
| 22 | Dolphin3.0-R1-Mistral-24B | 0.8678 |
| 23 | mistral-large-latest | 0.8672 |
| 24 | qwen3-235b-a22b | 0.8667 |
| 25 | glm-4.7 | 0.8661 |
| 26 | llama-3.1-405b | 0.8657 |
| 27 | o3-mini | 0.8654 |
| 28 | gpt-5-mini | 0.8651 |
| 29 | grok-4.1-fast | 0.8648 |
| 30 | claude-haiku-4-5-20251001-thinking | 0.8645 |
| 31 | o3 | 0.8642 |
| 32 | deepseek-v3-1-think-250821 | 0.8631 |
| 33 | llama-3.1-70b | 0.8562 |
| 34 | grok-4.1 | 0.8543 |
| 35 | kimi-k2 | 0.8412 |
| 36 | translategemma-4b | 0.8088 |
| 37 | llama-3-8b | 0.7626 |

### Short Text Leaderboard

| Rank | Model | Short Score |
|:----:|:------|:-----------:|
| 🥇 | **murasaki-14b-v0.2 (IQ4_XS, t=0.3)** | **0.8332** |
| 🥈 | **murasaki-4b-v0.2-nonthink (IQ4_XS, t=0.3)** | **0.8323** |
| 🥉 | **murasaki-8b-v0.2 (IQ4_XS, t=0.3)** | **0.8302** |
| 4 | murasaki-4b-v0.2-think (IQ4_XS, t=0.3) | 0.8283 |
| 5 | Sakura-qwen-2.5-14B (IQ4_XS, t=0.1) | 0.8282 |
| 6 | gemini-3-flash-preview | 0.8262 |
| 7 | gpt-4.1 | 0.8259 |
| 8 | claude-haiku-4-5-20251001-thinking | 0.8253 |
| 9 | qwen3-235b-a22b | 0.8250 |
| 10 | gpt-5-chat-latest | 0.8249 |
| 11 | gemini-2.5-flash | 0.8243 |
| 12 | claude-haiku-4-5-20251001 | 0.8239 |
| 13 | gemini-3-pro-preview | 0.8238 |
| 14 | claude-opus-4-5-20251101 | 0.8236 |
| 15 | qwen3-32b | 0.8211 |
| 16 | claude-sonnet-4-5-20250929 | 0.8208 |
| 17 | deepseek-v3.2 | 0.8199 |
| 18 | translategemma-12b | 0.8198 |
| 19 | deepseek-v3.2-thinking | 0.8179 |
| 20 | gemini-2.0-flash | 0.8176 |
| 21 | deepseek-v3.1 | 0.8144 |
| 22 | gpt-5-mini | 0.8139 |
| 23 | qwen3-14b | 0.8133 |
| 24 | deepseek-v3-1-think-250821 | 0.8118 |
| 25 | o3-mini | 0.8115 |
| 26 | Dolphin3.0-R1-Mistral-24B | 0.8108 |
| 27 | o3 | 0.8107 |
| 28 | glm-4.7 | 0.8102 |
| 29 | llama-3.1-70b | 0.8089 |
| 30 | grok-4.1 | 0.8088 |
| 31 | mistral-large-latest | 0.8084 |
| 32 | qwen3-8b | 0.8079 |
| 33 | llama-3.1-405b | 0.8077 |
| 34 | grok-4.1-fast | 0.8002 |
| 35 | translategemma-4b | 0.7923 |
| 36 | kimi-k2 | 0.7830 |
| 37 | llama-3-8b | 0.7198 |

Full results: [results/final_comet_scores.jsonl](results/final_comet_scores.jsonl)

---

## Key Features

* **Paragraph-Level Evaluation** — Two datasets (Short: 180-200 chars, Long: 780-800 chars) for comprehensive paragraph translation assessment.
* **Authoritative References** — Human translations from established fan groups and official Traditional Chinese releases.
* **COMET-Based Scoring** — Measures semantic alignment between LLM output and reference translations using neural evaluation.
* **Fair Comparison** — Standardized `temperature=1.0` and unified prompts ensure reproducible, comparable results.

---

## 🛠️ Methodology

### Data Pipeline

```mermaid
graph LR
    A[Official EPUB JP] --> C{Alignment}
    B[Fan/Official TL CN] --> C
    C -- Full Matrix DP + BGE-M3 --> D[High-Confidence Filtering]
    D --> E[Stratified Sampling]
    E --> F((Murasaki Dataset))
    
    style F fill:#f9f,stroke:#333,stroke-width:2px
```

### Data Post-processing
To ensure fair scoring, we apply rigorous **anomaly detection** to all model outputs before evaluation.
- **Empty Check**: Outputs that are completely empty are removed.
- **Length Ratio Check**: Outputs with a length ratio (Output/Source) `< 0.1` (too short) or `> 4.0` (hallucination loops) are excluded.
- **Safety Refusals**: Explicit refusals (e.g., "I cannot assist...") are treated as invalid and filtered.
*(This ensures that 0-score anomalies do not skew the distribution of valid translation scores.)*



> **⚠️ Known Issues**
> Some models exhibit significant issues in generation structure or content, resulting in a large number of samples being filtered out by the data cleaning process. Their final scores are calculated based on a small number of valid samples and **may not represent their true performance**:
> * **Qwen3-8B**: Extremely low valid rate (~24.5%), outputs contain excessive repetition or gibberish.
> * **Grok-4.1 / Grok-4.1-fast**: Valid rate only 50-60%, long text generation is highly unstable.
> * **DeepSeek-V3.1 / Qwen3-32B**: Low valid rate for long text, prone to truncation or formatting errors.

### Data Quality Report (Valid/Total)

| Model | Short | Long | Valid Rate |
|:------|:-----:|:----:|:----------:|
| claude-haiku-4-5-20251001 | 100/100 | 100/100 | 100.0% |
| claude-opus-4-5-20251101 | 100/100 | 100/100 | 100.0% |
| murasaki-8b-v0.1 | 100/100 | 100/100 | 100.0% |
| murasaki-8b-v0.2 | 100/100 | 100/100 | 100.0% |
| murasaki-14b-v0.2 | 100/100 | 100/100 | 100.0% |
| claude-haiku-4-5-20251001-thinking | 100/100 | 100/100 | 100.0% |
| Sakura-qwen-2.5-14B | 100/100 | 100/100 | 100.0% |
| gemini-3-pro-preview | 100/100 | 100/100 | 100.0% |
| gemini-3-flash-preview | 100/100 | 99/100 | 99.5% |
| glm-4.7 | 100/100 | 99/100 | 99.5% |
| kimi-k2 | 99/100 | 100/100 | 99.5% |
| deepseek-v3.2-thinking | 100/100 | 99/100 | 99.5% |
| translategemma-12b | 99/100 | 100/100 | 99.5% |
| gpt-4.1 | 100/100 | 98/100 | 99.0% |
| gemini-2.5-flash | 100/100 | 98/100 | 99.0% |
| gpt-5-chat-latest | 100/100 | 97/100 | 98.5% |
| o3 | 99/99 | 85/88 | 98.4% |
| o3-mini | 99/100 | 97/100 | 98.0% |
| claude-sonnet-4-5-20250929 | 96/100 | 99/100 | 97.5% |
| llama-3.1-70b | 100/100 | 94/100 | 97.0% |
| qwen3-14b | 98/100 | 90/100 | 94.0% |
| gpt-5-mini | 97/100 | 88/100 | 92.5% |
| translategemma-4b | 92/100 | 92/100 | 92.0% |
| Dolphin3.0-R1-Mistral-24B | 95/100 | 88/100 | 91.5% |
| deepseek-v3-1-think-250821 | 96/100 | 84/100 | 90.0% |
| mistral-large-latest | 95/100 | 84/100 | 89.5% |
| llama-3.1-405b | 90/100 | 80/100 | 85.0% |
| deepseek-v3.2 | 92/100 | 76/100 | 84.0% |
| gemini-2.0-flash | 97/100 | 67/100 | 82.0% |
| llama-3-8b | 85/100 | 78/100 | 81.5% |
| qwen3-32b | 91/100 | 56/100 | 73.5% |
| qwen3-235b-a22b | 92/100 | 52/100 | 72.0% |
| grok-4.1-fast | 72/100 | 46/100 | 59.0% |
| deepseek-v3.1 | 63/100 | 53/100 | 58.0% |
| grok-4.1 | 71/100 | 41/100 | 56.0% |
| qwen3-8b | 22/100 | 27/100 | 24.5% |

### Dataset Composition

| Category | Samples | Length (chars) | Content Type |
|----------|:-------:|:--------------:|--------------|
| **Short** | 100 | 180-200 | Dialogues, witty retorts, short descriptions |
| **Long** | 100 | 780-800 | Complex world-building, emotional monologues |

Covers major genres from commercial light novels and *Syosetu* web novels:

<details>
<summary><strong>🔍 Click to see Genre Coverage</strong></summary>

| Genre | Representative Works |
|-------|----------------------|
| **Isekai** | *Mushoku Tensei*, *TenSura*, *Shield Hero* |
| **RomCom** | *My Teen Romantic Comedy SNAFU*, *Oreimo*, *Kaguya-sama* |
| **Fantasy** | *SAO*, *KonoSuba*, *Spice and Wolf* |
| **Sci-Fi** | *86*, *Full Metal Panic* |
| **Slice of Life** | *Angel Next Door*, *Gimai Seikatsu* |
| **Mystery** | *Hyouka*, *Monogatari Series* |
| **War/Political** | *Youjo Senki*, *Legend of the Galactic Heroes* |

</details>

### Evaluation Protocol

| Parameter | Value |
|-----------|-------|
| Temperature | 1.0 |
| System Prompt | Standardized ([pipeline/config.py](pipeline/config.py)) |
| Special Cases | Sakura & Murasaki models use custom settings |
| Metric | COMET (Unbabel/wmt22-comet-da) |

---

## 📦 Dataset

The benchmark dataset is included in the [`data/`](data/) directory. Clone the repository to use it.

### File Structure

```text
data/
├── dataset_short.jsonl   # Short text benchmark (100 samples, 180-200 chars)
├── dataset_long.jsonl    # Long text benchmark (100 samples, 780-800 chars)
└── README.md             # Detailed dataset documentation
```

### Data Format (JSONL)

| Field | Type | Description |
|-------|------|-------------|
| `src` | string | Japanese source text |
| `ref` | string | Chinese reference translation |
| `category` | string | Category: `Short` or `Long` |

**Example**:
```json
{"src": "「そうだな、玄霧のほうが顔の造形に隙がない」", "ref": "「是啊，玄雾的脸型比较没有瑕疵。」", "category": "Short"}
```

> 📖 See [data/README.md](data/README.md) for full documentation.

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/soundstarrain/murasaki-benchmark
cd murasaki-benchmark
pip install -r requirements.txt
```

### Run Evaluation

**Option 1: Local Model (e.g., Qwen via Ollama)**
```bash
ollama pull qwen2.5:14b
python examples/local_llm_demo.py
```

**Option 2: API Provider**
```bash
cp .env.example .env
# Edit .env with your API credentials
python examples/api_eval_demo.py
```

> For detailed configuration, refer to [docs/local_deployment.md](docs/local_deployment.md).

---

## 📂 Project Structure

```text
murasaki-benchmark/
├── 📂 data/           # Benchmark datasets (Short/Long splits)
├── 📂 pipeline/       # Core evaluation logic (Prompting, Scoring)
├── 📂 examples/       # Minimal runnable scripts
├── 📂 results/        # Full evaluation logs & charts
└── 📂 docs/           # Detailed documentation
```

---

## 📝 Citation

If you find this benchmark useful, please cite our work:

```bibtex
@misc{murasaki2026,
  title={Murasaki Benchmark: An ACGN Translation Benchmark for LLMs},
  author={Murasaki Team},
  year={2026},
  url={https://github.com/soundstarrain/murasaki-benchmark}
}
```

---

## 📄 License

This project is licensed under the [GPL-3.0 License](LICENSE).

> The dataset is intended for **research purposes only**. Copyrights of the original novels and translations belong to their respective owners.
