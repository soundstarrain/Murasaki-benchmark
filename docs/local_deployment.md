# 添加本地LLM模型

本文档介绍如何将您的本地LLM模型添加到Murasaki Benchmark进行评测。

## 通用接口

本项目使用 **OpenAI兼容API** 作为统一接口，支持所有提供OpenAI格式API的本地LLM服务。

## 配置参数

在 `examples/local_llm_demo.py` 中配置您的模型：

```python
config = {
    "model_name": "your-model-name",      # 模型名称
    "api_key": "your-api-key",            # API密钥（本地服务通常任意值即可）
    "base_url": "http://localhost:8000/v1", # API地址
    "concurrency": 4                       # 并发数（根据显存调整）
}
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `model_name` | 模型标识符，用于API调用和结果保存 | `qwen2.5:14b`, `llama3.1:8b` |
| `api_key` | API密钥，本地服务通常填任意非空字符串 | `ollama`, `local` |
| `base_url` | API端点地址，必须以 `/v1` 结尾 | `http://localhost:11434/v1` |
| `concurrency` | 并发请求数，根据显存和模型大小调整 | `1-8` |

## 常见本地LLM服务配置

### Ollama

```python
config = {
    "model_name": "qwen2.5:14b",
    "api_key": "ollama",
    "base_url": "http://localhost:11434/v1",
    "concurrency": 2
}
```

### vLLM

```python
config = {
    "model_name": "Qwen/Qwen2.5-14B-Instruct",
    "api_key": "vllm",
    "base_url": "http://localhost:8000/v1",
    "concurrency": 4
}
```

### llama.cpp (llama-server)

```python
config = {
    "model_name": "local-model",
    "api_key": "llamacpp",
    "base_url": "http://localhost:8080/v1",
    "concurrency": 1
}
```

### LM Studio

```python
config = {
    "model_name": "local-model",
    "api_key": "lm-studio",
    "base_url": "http://localhost:1234/v1",
    "concurrency": 1
}
```

### Text Generation WebUI (oobabooga)

```python
config = {
    "model_name": "local-model",
    "api_key": "ooba",
    "base_url": "http://localhost:5000/v1",
    "concurrency": 1
}
```

## 运行评测

```bash
python examples/local_llm_demo.py
```

结果将保存到 `results/` 目录。

## 添加到批量评测

如需将本地模型加入批量评测，编辑 `pipeline/config.py`：

```python
MODELS_TO_EVAL = [
    # 云端模型
    "gpt-4o",
    "claude-sonnet-4-20250514",
    
    # 添加您的本地模型
    "qwen2.5:14b",  
    "your-local-model",
]
```

然后修改 `pipeline/config.py` 中的 API 配置指向您的本地服务。

## 注意事项

1. **确保API兼容性**: 您的本地服务需支持 `/v1/chat/completions` 端点
2. **调整并发数**: 根据显存大小调整 `concurrency`，避免OOM
3. **超时设置**: 本地推理较慢，如遇超时可在代码中增加timeout值
