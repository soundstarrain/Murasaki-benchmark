# 评测结果说明

## 目录结构

```
results/
├── final_comet_scores.csv       # COMET分数汇总
├── final_comet_scores.jsonl     # COMET分数详细数据
├── model_comparison_report.html # 可视化对比报告
├── murasaki_benchmark_chart.png # 评测结果图表
└── models/                      # 各模型详细结果
    ├── gpt-5-chat-latest/
    │   ├── gpt-5-chat-latest_run1.csv
    │   ├── gpt-5-chat-latest_run2.csv
    │   └── gpt-5-chat-latest_run3.csv
    └── ...
```

## 结果文件格式

### 模型结果CSV

每个模型的结果文件包含以下列：

| 列名 | 说明 |
|------|------|
| `src` | 日语源文本 |
| `ref` | 中文参考译文 |
| `model_output` | 模型生成的译文 |
| `category` | 类别 (Short/Long) |
| `comet_score` | 句子级COMET分数 |

### COMET分数汇总

`final_comet_scores.csv` 包含：

| 列名 | 说明 |
|------|------|
| `model_name` | 模型名称 |
| `comet` | 系统级COMET分数 |
| `Short_comet` | 短文本COMET |
| `Long_comet` | 长文本COMET |

## 评测说明

- 使用 Unbabel/wmt22-comet-da 模型计算COMET分数
- COMET分数范围通常在0-1之间，越高表示翻译质量越好
