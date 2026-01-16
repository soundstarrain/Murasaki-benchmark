"""
Murasaki Benchmark - 本地LLM评测示例

本示例演示如何使用本地部署的LLM进行翻译评测。
支持 Ollama、vLLM、llama.cpp 等兼容 OpenAI API 的本地服务。

使用前请确保:
1. 已安装并运行本地LLM服务
2. 已安装项目依赖: pip install -r requirements.txt
"""

import asyncio
import pandas as pd
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.generator import LLMGenerator
from pipeline.evaluator import evaluate_metrics
from pipeline.config import SYSTEM_PROMPT


# ============================================================
# 配置区 - 根据你的本地LLM服务修改
# ============================================================

# Ollama 配置示例
OLLAMA_CONFIG = {
    "model_name": "qwen2.5:14b",  # 或 "llama3.1:8b", "mistral:7b" 等
    "api_key": "ollama",  # Ollama不需要真实API key
    "base_url": "http://localhost:11434/v1",
    "concurrency": 2  # 本地并发数，根据显存调整
}

# vLLM 配置示例
VLLM_CONFIG = {
    "model_name": "Qwen/Qwen2.5-14B-Instruct",
    "api_key": "vllm",
    "base_url": "http://localhost:8000/v1",
    "concurrency": 4
}

# llama.cpp (llama-server) 配置示例
LLAMACPP_CONFIG = {
    "model_name": "local-model",
    "api_key": "llamacpp",
    "base_url": "http://localhost:8080/v1",
    "concurrency": 1
}


async def run_local_eval(config: dict, dataset_path: str = "data/dataset_short.jsonl"):
    """
    使用本地LLM运行评测
    
    Args:
        config: LLM配置字典
        dataset_path: 数据集路径
    """
    print(f"=" * 60)
    print(f"本地LLM评测 - {config['model_name']}")
    print(f"服务地址: {config['base_url']}")
    print(f"=" * 60)
    
    # 1. 加载数据集
    print(f"\n[1/4] 加载数据集: {dataset_path}")
    with open(dataset_path, 'r', encoding='utf-8') as f:
        import json
        data = [json.loads(line) for line in f]
    dataset = pd.DataFrame(data)
    print(f"  样本数: {len(dataset)}")
    
    # 可选：只评测前N条（快速测试）
    # dataset = dataset.head(10)
    # print(f"  [测试模式] 仅评测前10条")
    
    # 2. 初始化生成器
    print(f"\n[2/4] 初始化LLM生成器...")
    generator = LLMGenerator(config)
    
    # 3. 生成翻译
    print(f"\n[3/4] 生成翻译中...")
    results = await generator.generate_batch(dataset, SYSTEM_PROMPT)
    
    # 4. 评估结果
    print(f"\n[4/4] 计算COMET分数...")
    eval_result = evaluate_metrics(results)
    
    # 输出结果
    print(f"\n{'=' * 60}")
    print(f"评测结果 - {config['model_name']}")
    print(f"{'=' * 60}")
    print(f"  COMET: {eval_result['comet']:.4f}")
    
    if 'category_scores' in eval_result and eval_result['category_scores']:
        print(f"\n分类别得分:")
        for cat, scores in eval_result['category_scores'].items():
            print(f"  {cat}: COMET={scores['comet']:.4f}")
    
    # 保存结果
    output_path = f"results/{config['model_name'].replace('/', '_')}_local.csv"
    os.makedirs("results", exist_ok=True)
    eval_result['results_df'].to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n结果已保存: {output_path}")
    
    return eval_result


def main():
    """主函数 - 选择配置并运行"""
    
    print("Murasaki Benchmark - 本地LLM评测工具")
    print("-" * 40)
    print("可用配置:")
    print("  1. Ollama (默认)")
    print("  2. vLLM")
    print("  3. llama.cpp")
    print()
    
    # 默认使用Ollama配置
    config = OLLAMA_CONFIG
    
    # 运行评测
    asyncio.run(run_local_eval(config))


if __name__ == "__main__":
    main()
