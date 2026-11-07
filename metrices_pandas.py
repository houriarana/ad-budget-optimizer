import pandas as pd
import time
import os


def analyze_with_pandas(file_path):
    print(f"\n{'='*60}")
    print(f"🐼 Pandas Analysis: {os.path.basename(file_path)}")
    print(f"{'='*60}")

    start = time.time()

    # Chunked reading = memory crash se bachne ke liye (bade data ke liye zaroori!)
    chunks = []
    for chunk in pd.read_csv(file_path, chunksize=500_000):
        chunk["ctr"] = chunk["clicks"] / chunk["impressions"].replace(0, 1)
        chunk["cpc"] = chunk["spend"] / chunk["clicks"].replace(0, 1)
        chunk["cpa"] = chunk["spend"] / chunk["conversions"].replace(0, 1)
        chunk["cvr"] = chunk["conversions"] / chunk["clicks"].replace(0, 1)
        chunk["roas"] = chunk["revenue"] / chunk["spend"].replace(0, 1)
        chunks.append(chunk)

    df = pd.concat(chunks, ignore_index=True)
    load_time = time.time() - start

    # Platform-wise aggregate
    platform_summary = df.groupby("platform").agg(
        total_spend=("spend", "sum"),
        total_revenue=("revenue", "sum"),
        total_clicks=("clicks", "sum"),
        total_impressions=("impressions", "sum"),
        total_conversions=("conversions", "sum"),
    ).reset_index()

    platform_summary["CTR"]  = platform_summary["total_clicks"] / platform_summary["total_impressions"]
    platform_summary["CPC"]  = platform_summary["total_spend"] / platform_summary["total_clicks"]
    platform_summary["CPA"]  = platform_summary["total_spend"] / platform_summary["total_conversions"]
    platform_summary["CVR"]  = platform_summary["total_conversions"] / platform_summary["total_clicks"]
    platform_summary["ROAS"] = platform_summary["total_revenue"] / platform_summary["total_spend"]

    platform_summary = platform_summary.sort_values("ROAS", ascending=False)

    total_time = time.time() - start
    print(f"⏱️  Load + Process Time: {load_time:.2f}s  |  Total: {total_time:.2f}s")
    print(f"📊 Rows processed: {len(df):,}")
    print("\n" + platform_summary.round(3).to_string(index=False))

    return platform_summary, total_time


if __name__ == "__main__":
    # Hum abhi 10 Lakh (1M) wali file par test karenge
    file_to_check = "data/ads_1m.csv" 
    
    if os.path.exists(file_to_check):
        analyze_with_pandas(file_to_check)
    else:
        print("File nahi mili, pehle data_generator.py chalayein.")