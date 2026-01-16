from comet import download_model, load_from_checkpoint
import torch
import pandas as pd

# Global model loading - singleton pattern
COMET_MODEL_PATH = None
comet_model = None

def load_comet():
    """Load COMET model (singleton, only loads once)"""
    global comet_model, COMET_MODEL_PATH
    if comet_model is not None:
        return

    print("Loading COMET model...")
    try:
        COMET_MODEL_PATH = download_model("Unbabel/wmt22-comet-da")
        comet_model = load_from_checkpoint(COMET_MODEL_PATH)
        if torch.cuda.is_available():
            comet_model = comet_model.to("cuda")
        print("COMET model loaded successfully.")
    except Exception as e:
        print(f"Failed to load COMET model: {e}")
        comet_model = None


def evaluate_metrics(df):
    """
    Evaluate translation quality using COMET.
    
    Input df columns: src, ref, model_output, model_name, [category]
    Returns: dict with comet score, category scores, and results dataframe
    """
    # Ensure model is loaded
    load_comet()

    refs = df['ref'].tolist()
    hyps = df['model_output'].tolist()
    srcs = df['src'].tolist()

    # Calculate COMET
    comet_score_sys = 0.0
    comet_scores_seg = [0.0] * len(df)

    if comet_model is not None:
        data = [{"src": s, "mt": m, "ref": r} for s, m, r in zip(srcs, hyps, refs)]
        print("Calculating COMET scores...")
        batch_size = 8
        try:
            comet_output = comet_model.predict(
                data, 
                batch_size=batch_size, 
                gpus=1 if torch.cuda.is_available() else 0
            )
            comet_score_sys = comet_output.system_score
            comet_scores_seg = comet_output.scores
        except Exception as e:
            print(f"Error calculating COMET: {e}")
    else:
        print("COMET model not available, skipping COMET calculation.")

    # Add scores to DataFrame
    df_result = df.copy()
    df_result['comet_score'] = comet_scores_seg

    # Calculate Category-wise Metrics if 'category' column exists
    category_scores = {}
    if 'category' in df_result.columns:
        print("Calculating categorized scores...")
        for cat, group in df_result.groupby('category'):
            cat_comet = group['comet_score'].mean()
            category_scores[cat] = {"comet": cat_comet}

    return {
        "comet": comet_score_sys,
        "category_scores": category_scores,
        "results_df": df_result
    }
