# 评测结果说明

## 目录结构

```
results/
├── final_comet_scores.csv       # XCOMET分数汇总
├── final_comet_scores.jsonl     # XCOMET分数详细数据
├── model_comparison_report.html # 可视化对比报告
├── murasaki_benchmark_chart.png # 评测结果图表
└── models/                      # 各模型详细结果
    └── <model_name>/
        ├── dataset_Short_run1.jsonl  # 短文本评测结果
        └── dataset_Long_run1.jsonl   # 长文本评测结果
```

## 结果文件格式

### 模型结果JSONL

每个模型的结果文件为JSONL格式，每行包含以下字段：

| 字段 | 说明 |
|------|------|
| `src` | 日语源文本 |
| `ref` | 中文参考译文 |
| `category` | 类别 (Short/Long) |
| `model_output` | 模型生成的译文 |
| `model_name` | 模型名称 |

> **注意**: XCOMET分数在评测流程中计算，汇总保存在 `final_comet_scores.csv` 中，不单独存储在每条记录。

### XCOMET分数汇总

`final_comet_scores.csv` 包含：

| 列名 | 说明 |
|------|------|
| `model_name` | 模型名称 |
| `comet` | 系统级XCOMET分数 |
| `Short_comet` | 短文本XCOMET |
| `Long_comet` | 长文本XCOMET |

## 评测说明

- 使用 Unbabel/XCOMET-XL 模型计算XCOMET分数
- XCOMET分数范围通常在0-1之间，越高表示翻译质量越好
