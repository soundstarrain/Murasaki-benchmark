import os
from dotenv import load_dotenv

load_dotenv()

# 评测数据集路径
DATASET_SHORT = "data/dataset_short.jsonl"
DATASET_LONG = "data/dataset_long.jsonl"

# 默认数据集（合并Short和Long）
DATASET_PATH = "data/dataset_short.jsonl"  # 可替换为 DATASET_LONG

# 通用 System Prompt
SYSTEM_PROMPT = """你是一个精通日本轻小说的专业翻译模型。
请将给定的文本翻译成日本轻小说风格的简体中文。

### 输出格式
符号采用半角数字和直角引号如「 」,
仅输出翻译后的正文。单行文本，不需要换行符号。"""

# 全局 API 配置
GLOBAL_API_KEY = os.getenv("OPENAI_API_KEY")
GLOBAL_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
GLOBAL_CONCURRENCY = 30

# 模型列表
MODELS_TO_EVAL = [
    "gemini-2.0-flash",
    "qwen3-14b", "Qwen3-8B", "llama-3.1-405b", "llama-3-8b", "kimi-k2",
    "gpt-5-chat-latest", "gpt-5-mini", "o3", "o3-mini", "gpt-4.1",  
    "claude-haiku-4-5-20251001", "claude-haiku-4-5-20251001-thinking",
    "claude-opus-4-5-20251101", "claude-sonnet-4-5-20250929",
    "gemini-3-flash-preview", "gemini-3-pro-preview", "gemini-2.5-flash",
    "deepseek-v3.2", "deepseek-v3.2-thinking", "deepseek-v3-1-think-250821", "deepseek-v3.1", 
    "Dolphin3.0-R1-Mistral-24B", "mistral-large-latest",
    "qwen3-32b", "qwen3-235b-a22b",
    "glm-4.7", "grok-4.1", "grok-4.1-fast", "llama-3.1-70b", 
]