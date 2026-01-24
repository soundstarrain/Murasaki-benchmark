import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import seaborn as sns

# Configuration
OUTPUT_IMAGE = "results/murasaki_benchmark_chart.png"
TITLE = "Murasaki-ACGN: A Benchmark for Japanese-Chinese ACGN Translation"

# Auto-detect input file
INPUT_FILE = "results/final_comet_scores.csv"
if os.path.exists("results/leaderboard_xcomet.csv"):
    INPUT_FILE = "results/leaderboard_xcomet.csv"
    print(f"Detected XCOMET evaluation results: {INPUT_FILE}")

def setup_chinese_font():
    """Attempt to set a Chinese font for Matplotlib on Windows."""
    # Common Windows Chinese fonts
    font_names = ["Microsoft YaHei", "SimHei", "Malgun Gothic", "SimSun"]
    
    # Try to find a valid font path
    found_font = None
    for name in font_names:
        try:
            # Check if font is available in system paths
            font_path = fm.findfont(fm.FontProperties(family=name))
            available = [f.name for f in fm.fontManager.ttflist]
            if name in available:
                found_font = name
                break
        except:
            continue
            
    if found_font:
        plt.rcParams['font.family'] = [found_font, 'sans-serif']
        print(f"Using font: {found_font}")
    else:
        print("Warning: Common Chinese fonts not found in Matplotlib cache. Trying 'Microsoft YaHei' directly.")
        plt.rcParams['font.family'] = ['Microsoft YaHei', 'SimHei', 'sans-serif']
        plt.rcParams['axes.unicode_minus'] = False

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Please run evaluation first.")
        return

    # 1. Load Data
    try:
        df = pd.read_csv(INPUT_FILE)
    except Exception as e:
        print(f"Error reading {INPUT_FILE}: {e}")
        return
    
    # 2. Sort by Avg Score Descending
    if "comet" in df.columns:
        df = df.sort_values(by="comet", ascending=False).reset_index(drop=True)
    
    # Add Rank to Model Name for display
    df["display_name"] = (df.index + 1).astype(str) + ". " + df["model_name"]

    # 3. Setup Plot
    setup_chinese_font()
    sns.set_theme(style="whitegrid")
    setup_chinese_font() # Re-apply after theme set

    # Melt for plotting
    # Columns expected: comet (avg), Short_comet, Long_comet
    value_vars = ["comet"]
    if "Short_comet" in df.columns: value_vars.append("Short_comet")
    if "Long_comet" in df.columns: value_vars.append("Long_comet")
    
    df_melt = df.melt(id_vars=["display_name", "model_name"], 
                      value_vars=value_vars, 
                      var_name="Metric", 
                      value_name="Score")
    
    metric_map = {
        "comet": "Overall Avg",
        "Short_comet": "Short",
        "Long_comet": "Long"
    }
    df_melt["Metric"] = df_melt["Metric"].map(metric_map)

    # Dynamic Height
    height = len(df) * 0.6 + 2
    plt.figure(figsize=(14, height))

    # 4. Create Horizontal Bar Plot
    chart = sns.barplot(
        data=df_melt,
        x="Score",
        y="display_name",
        hue="Metric",
        hue_order=["Overall Avg", "Short", "Long"],
        palette="viridis",
        edgecolor="w" 
    )
    
    # ADD VALUE LABELS
    for container in chart.containers:
        chart.bar_label(container, fmt='%.4f', padding=3, fontsize=9)

    # 5. Styling
    plt.title(TITLE, fontsize=20, fontweight='bold', pad=20)
    plt.xlabel("COMET Score (Unbabel/wmt22-comet-da)", fontsize=14)
    plt.ylabel("", fontsize=12) 
    plt.legend(title="Metric", bbox_to_anchor=(1.0, 1.02), loc='upper left', fontsize=11)
    
    # Adjust X Limits
    # Find min score to set sensible x lim
    min_score = df_melt["Score"].min()
    if pd.isna(min_score): min_score = 0
    xlim_min = int(min_score * 20) / 20 - 0.05
    plt.xlim(max(0, xlim_min), 1.0) # Cap at 1.0 MAX
    
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # 6. Save
    os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)
    plt.savefig(OUTPUT_IMAGE, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
