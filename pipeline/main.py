import asyncio
import os
import pandas as pd
import json

# 使用相对导入（从pipeline目录运行）或绝对导入
try:
    from pipeline.config import MODELS_TO_EVAL, DATASET_SHORT, DATASET_LONG, SYSTEM_PROMPT, GLOBAL_API_KEY, GLOBAL_BASE_URL, GLOBAL_CONCURRENCY
    from pipeline.generator import LLMGenerator
    from pipeline.evaluator import evaluate_metrics
except ImportError:
    from config import MODELS_TO_EVAL, DATASET_SHORT, DATASET_LONG, SYSTEM_PROMPT, GLOBAL_API_KEY, GLOBAL_BASE_URL, GLOBAL_CONCURRENCY
    from generator import LLMGenerator
    from evaluator import evaluate_metrics


def load_jsonl(path):
    """Load a JSONL file and return list of dicts."""
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


async def main():
    # 1. Load Datasets (Short + Long)
    print(f"Loading datasets...")
    try:
        data_short = load_jsonl(DATASET_SHORT)
        data_long = load_jsonl(DATASET_LONG)
        data = data_short + data_long
        dataset = pd.DataFrame(data)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    print(f"Loaded {len(dataset)} examples (Short: {len(data_short)}, Long: {len(data_long)}).")
    if 'category' in dataset.columns:
        print(f"Categories found: {dataset['category'].unique()}")
    
    # Prepare results directory
    results_dir = "results/models"
    os.makedirs(results_dir, exist_ok=True)
    
    leaderboard = []

    # 2. Iterate Models
    for model_name in MODELS_TO_EVAL:
        safe_model_name = model_name.replace("/", "_").replace(":", "_")
        
        # Prepare Model Config
        model_config = {
            "model_name": model_name,
            "api_key": GLOBAL_API_KEY,
            "base_url": GLOBAL_BASE_URL,
            "concurrency": GLOBAL_CONCURRENCY
        }
        
        print(f"\n=== Processing Model: {model_name} ===")

        # Create model-specific directory
        model_results_dir = os.path.join(results_dir, safe_model_name)
        os.makedirs(model_results_dir, exist_ok=True)
        
        result_file_path = os.path.join(model_results_dir, f"{safe_model_name}_run1.csv")
        
        # Check for existing results
        if os.path.exists(result_file_path):
            print(f"Found existing results at {result_file_path}. Skipping generation.")
            df_result = pd.read_csv(result_file_path)
        else:
            print(f"No existing results found. Generating...")
            generator = LLMGenerator(model_config)
            df_result = await generator.generate_batch(dataset, SYSTEM_PROMPT)
            df_result.to_csv(result_file_path, index=False, encoding='utf-8-sig')
            print(f"Generation complete. Saved to {result_file_path}")

        # 3. Evaluate
        print(f"Evaluating {model_name}...")
        
        if 'comet_score' not in df_result.columns:
            eval_result = evaluate_metrics(df_result)
            eval_result['results_df'].to_csv(result_file_path, index=False, encoding='utf-8-sig')
        else:
            eval_result = evaluate_metrics(df_result)

        # Collect Scores
        run_scores = {
            "model_name": model_name,
            "comet": eval_result['comet']
        }
        
        # Add Category Scores
        if 'category_scores' in eval_result and eval_result['category_scores']:
            for cat, metrics in eval_result['category_scores'].items():
                run_scores[f"{cat}_comet"] = metrics['comet']

        leaderboard.append(run_scores)
        print(f"Scores: COMET={run_scores['comet']:.4f}")

    # 4. Save Final Leaderboard
    leaderboard_df = pd.DataFrame(leaderboard)
    leaderboard_df = leaderboard_df.sort_values(by='comet', ascending=False)
    
    leaderboard_path = "results/leaderboard.csv"
    leaderboard_df.to_csv(leaderboard_path, index=False, encoding='utf-8-sig')
    
    print("\n=== Final Leaderboard ===")
    print(leaderboard_df)
    print(f"Leaderboard saved to {leaderboard_path}")


if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
