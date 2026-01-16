"""
Murasaki Benchmark - 云端API评测示例

本示例演示如何使用云端LLM API进行翻译评测。
支持 OpenAI、Claude、Gemini 等兼容 OpenAI API 格式的服务。

使用前请确保:
1. 已配置 .env 文件中的 API 密钥
2. 已安装项目依赖: pip install -r requirements.txt
"""

import asyncio
import pandas as pd
import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.generator import LLMGenerator
from pipeline.evaluator import evaluate_metrics
from pipeline.config import SYSTEM_PROMPT


# ============================================================
# 配置区 - 根据你的API服务修改
# ============================================================

# OpenAI 配置
OPENAI_CONFIG = {
    "model_name": "gpt-4o",
    "api_key": os.getenv("OPENAI_API_KEY"),
    "base_url": "https://api.openai.com/v1",
    "concurrency": 10
}

# Claude (通过兼容API)
CLAUDE_CONFIG = {
    "model_name": "claude-sonnet-4-20250514",
    "api_key": os.getenv("ANTHROPIC_API_KEY"),
    "base_url": os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1"),
    "concurrency": 5
}

# Gemini (通过兼容API)
GEMINI_CONFIG = {
    "model_name": "gemini-2.0-flash",
    "api_key": os.getenv("GOOGLE_API_KEY"),
    "base_url": os.getenv("GOOGLE_BASE_URL"),
    "concurrency": 10
}

# 通用OpenAI兼容API (如OpenRouter、Together等)
GENERIC_CONFIG = {
    "model_name": os.getenv("MODEL_NAME", "gpt-4o"),
    "api_key": os.getenv("OPENAI_API_KEY"),
    "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    "concurrency": int(os.getenv("CONCURRENCY", "10"))
}


async def run_api_eval(config: dict, dataset_path: str = "data/dataset_short.jsonl"):
    """
    使用云端API运行评测
    
    Args:
        config: LLM配置字典
        dataset_path: 数据集路径
    """
    # 验证API key
    if not config.get("api_key"):
        print(f"错误: 未配置API密钥，请检查.env文件")
        return None
    
    print(f"=" * 60)
    print(f"云端API评测 - {config['model_name']}")
    print(f"服务地址: {config['base_url']}")
    print(f"=" * 60)
    
    # 1. 加载数据集
    print(f"\n[1/4] 加载数据集: {dataset_path}")
    with open(dataset_path, 'r', encoding='utf-8') as f:
        import json
        data = [json.loads(line) for line in f]
    dataset = pd.DataFrame(data)
    print(f"  样本数: {len(dataset)}")
    
    # 2. 初始化生成器
    print(f"\n[2/4] 初始化LLM生成器...")
    generator = LLMGenerator(config)
    
    # 3. 生成翻译
    print(f"\n[3/4] 生成翻译中 (并发数: {config['concurrency']})...")
    results = await generator.generate_batch(dataset, SYSTEM_PROMPT)
    
    # 4. 评估结果
    print(f"\n[4/4] 计算COMET分数...")
    eval_result = evaluate_metrics(results)
    
    # 输出结果
    print(f"\n{'=' * 60}")
    print(f"评测结果 - {config['model_name']}")
    print(f"{'=' * 60}")
    print(f"  COMET: {eval_result['comet']:.4f}")
    
    # 保存结果
    safe_name = config['model_name'].replace('/', '_').replace(':', '_')
    output_path = f"results/{safe_name}_api.csv"
    os.makedirs("results", exist_ok=True)
    eval_result['results_df'].to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n结果已保存: {output_path}")
    
    return eval_result


def main():
    """主函数"""
    print("Murasaki Benchmark - 云端API评测工具")
    print("-" * 40)
    
    # 使用通用配置（从.env读取）
    config = GENERIC_CONFIG
    
    print(f"模型: {config['model_name']}")
    print(f"API: {config['base_url']}")
    
    # 运行评测
    asyncio.run(run_api_eval(config))


if __name__ == "__main__":
    main()
