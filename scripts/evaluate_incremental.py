import os
import json
import pandas as pd
import sys

# Ensure we can import from pipeline
dataset_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dataset_root)

try:
    from pipeline.evaluator import evaluate_metrics
except ImportError:
    print("Error: Could not import pipeline.evaluator. Make sure you are running from the project root or scripts directory.")
    sys.exit(1)

RESULTS_DIR = os.path.join(dataset_root, "results")
MODELS_DIR = os.path.join(RESULTS_DIR, "models")
CSV_PATH = os.path.join(RESULTS_DIR, "final_comet_scores.csv")
JSONL_PATH = os.path.join(RESULTS_DIR, "final_comet_scores.jsonl")

def load_jsonl(path):
    data = []
    if not os.path.exists(path):
        return data
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except:
                    continue
    return data

def main():
    # 1. Load Existing Results
    existing_models = set()
    if os.path.exists(CSV_PATH):
        try:
            df_existing = pd.read_csv(CSV_PATH)
            if 'model_name' in df_existing.columns:
                existing_models = set(df_existing['model_name'].astype(str))
            print(f"Loaded {len(existing_models)} existing models from leaderboard.")
        except Exception as e:
            print(f"Warning: Could not read existing CSV: {e}")
    else:
        print("No existing leaderboard found. Fresh start.")

    # 2. Scan for New Models
    if not os.path.exists(MODELS_DIR):
        print(f"Models directory not found: {MODELS_DIR}")
        return

    all_model_dirs = [d for d in os.listdir(MODELS_DIR) if os.path.isdir(os.path.join(MODELS_DIR, d))]
    new_models = [m for m in all_model_dirs if m not in existing_models]
    
    if not new_models:
        print("No new models found to evaluate.")
        return

    print(f"Found {len(new_models)} new models: {', '.join(new_models)}")
    
    new_results = []

    # 3. Evaluate New Models
    for model_name in sorted(new_models):
        print(f"\n=== Evaluating: {model_name} ===")
        model_path = os.path.join(MODELS_DIR, model_name)
        
        # Merge all jsonl files in the model folder
        jsonl_files = [f for f in os.listdir(model_path) if f.endswith('.jsonl')]
        if not jsonl_files:
            print(f"  Skipping (no .jsonl output files)")
            continue
            
        all_data = []
        for jf in jsonl_files:
            all_data.extend(load_jsonl(os.path.join(model_path, jf)))
            
        if not all_data:
            print("  Skipping (empty data)")
            continue
            
        df = pd.DataFrame(all_data)
        print(f"  Loaded {len(df)} samples")
        
        try:
            # Run Evaluation
            eval_result = evaluate_metrics(df)
            
            run_scores = {
                "model_name": model_name,
                "comet": eval_result['comet']
            }
            if 'category_scores' in eval_result:
                for cat, metrics in eval_result['category_scores'].items():
                    run_scores[f"{cat}_comet"] = metrics.get('comet', 0.0)
            
            new_results.append(run_scores)
            print(f"  Score: {run_scores['comet']:.4f}")
            
        except Exception as e:
            print(f"  Evaluation failed: {e}")
            import traceback
            traceback.print_exc()

    # 4. Append and Save
    if new_results:
        # Load existing (again, to be safe) or init empty
        if os.path.exists(CSV_PATH):
            df_final = pd.read_csv(CSV_PATH)
        else:
            df_final = pd.DataFrame()
            
        df_new = pd.DataFrame(new_results)
        
        # Concatenate
        df_final = pd.concat([df_final, df_new], ignore_index=True)
        
        # Deduplicate (keep latest just in case)
        if 'model_name' in df_final.columns:
            df_final = df_final.drop_duplicates(subset=['model_name'], keep='last')
            
        # Sort
        if 'comet' in df_final.columns:
            df_final = df_final.sort_values(by='comet', ascending=False)
            
        # Save CSV
        df_final.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')
        
        # Save JSONL
        with open(JSONL_PATH, 'w', encoding='utf-8') as f:
            for _, row in df_final.iterrows():
                f.write(json.dumps(row.to_dict(), ensure_ascii=False) + '\n')
                
        print(f"\nUpdated leaderboard saved with {len(new_results)} new entries.")
        print(df_final[['model_name', 'comet']].head().to_string())
    else:
        print("\nNo valid results produced.")

if __name__ == "__main__":
    main()
