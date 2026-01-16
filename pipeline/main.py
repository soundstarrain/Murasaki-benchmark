import asyncio
import os
import pandas as pd
import json

# Handle imports whether run as module or script
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
    data = []
    if not os.path.exists(path):
        return data
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return data


async def main():
    # 1. Load Datasets (Short + Long)
    print(f"Loading datasets...")
    try:
        data_short = load_jsonl(DATASET_SHORT)
        data_long = load_jsonl(DATASET_LONG)
        
        # Ensure categories are set correctly
        for item in data_short:
            item['category'] = 'Short'
        for item in data_long:
            item['category'] = 'Long'
            
        df_short_source = pd.DataFrame(data_short)
        df_long_source = pd.DataFrame(data_long)
        
    except Exception as e:
        print(f"Error loading source datasets: {e}")
        return

    print(f"Loaded source data: Short={len(df_short_source)}, Long={len(df_long_source)}")
    
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
        
        # Define result file paths
        short_result_path = os.path.join(model_results_dir, "dataset_Short_run1.jsonl")
        long_result_path = os.path.join(model_results_dir, "dataset_Long_run1.jsonl")
        
        generator = LLMGenerator(model_config)

        # --- Process Short Dataset ---
        print(f"  [Short] Processing...")
        # Check if generation is needed/complete for Short
        # The generator's generate_batch handles incremental saving and skipping existing
        if len(df_short_source) > 0:
            df_short_result = await generator.generate_batch(
                df_short_source, 
                SYSTEM_PROMPT, 
                save_path=short_result_path
            )
        else:
            df_short_result = pd.DataFrame()

        # --- Process Long Dataset ---
        print(f"  [Long] Processing...")
        if len(df_long_source) > 0:
            df_long_result = await generator.generate_batch(
                df_long_source, 
                SYSTEM_PROMPT, 
                save_path=long_result_path
            )
        else:
            df_long_result = pd.DataFrame()

        # --- Combine for Evaluation ---
        df_result = pd.concat([df_short_result, df_long_result], ignore_index=True)
        
        if len(df_result) == 0:
            print("  No results to evaluate.")
            continue

        # 3. Evaluate
        print(f"  Evaluating {len(df_result)} samples...")
        
        # Note: evaluate_metrics calculates scores but we don't save them back to row-level files
        # based on user requirement (scores in summary only).
        eval_result = evaluate_metrics(df_result)

        # Collect Scores
        run_scores = {
            "model_name": model_name,
            "comet": eval_result.get('comet', 0.0)
        }
        
        # Add Category Scores
        if 'category_scores' in eval_result and eval_result['category_scores']:
            for cat, metrics in eval_result['category_scores'].items():
                run_scores[f"{cat}_comet"] = metrics.get('comet', 0.0)

        leaderboard.append(run_scores)
        print(f"  Scores: COMET={run_scores['comet']:.4f}")

    # 4. Save Final Leaderboard
    leaderboard_df = pd.DataFrame(leaderboard)
    if not leaderboard_df.empty and 'comet' in leaderboard_df.columns:
        leaderboard_df = leaderboard_df.sort_values(by='comet', ascending=False)
    
    leaderboard_path = "results/final_comet_scores.csv"
    leaderboard_df.to_csv(leaderboard_path, index=False, encoding='utf-8-sig')
    
    print("\n=== Final Leaderboard ===")
    print(leaderboard_df)
    print(f"Leaderboard saved to {leaderboard_path}")


if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
