import argparse
import os, json
import pandas as pd
import matplotlib.pyplot as plt

def analyze(input_path: str, outdir: str):
    os.makedirs(outdir, exist_ok=True)

    # Load
    df = pd.read_csv(input_path, parse_dates=["date"])
    # Clean
    df_clean = df.dropna().copy()
    # Summary
    summary = {
        "rows_before": len(df),
        "rows_after": len(df_clean),
        "columns": list(df_clean.columns),
        "describe_value1": df_clean["value1"].describe().to_dict(),
        "describe_value2": df_clean["value2"].describe().to_dict(),
    }
    with open(os.path.join(outdir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # Save cleaned
    df_clean.to_csv(os.path.join(outdir, "cleaned.csv"), index=False)

    # Histogram of value1
    plt.figure()
    df_clean["value1"].hist(bins=20)
    plt.title("Histogram of value1")
    plt.xlabel("value1")
    plt.ylabel("frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "hist_value1.png"))
    plt.close()

    # Line plot of value2 over time
    plt.figure()
    df_clean.sort_values("date").set_index("date")["value2"].plot()
    plt.title("value2 over time")
    plt.xlabel("date")
    plt.ylabel("value2")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "line_value2.png"))
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/sample_data.csv", help="Path to input CSV")
    parser.add_argument("--outdir", default="outputs", help="Directory to write outputs")
    args = parser.parse_args()
    analyze(args.input, args.outdir)
