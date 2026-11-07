import pandas as pd
import os

def recommend_budget(file_path, total_budget=1_000_000):
    print(f"\n{'='*65}")
    print(f"💰 BUDGET RECOMMENDATION ENGINE")
    print(f"   Total Budget: Rs. {total_budget:,.0f}")
    print(f"{'='*65}")

    chunks = []
    for chunk in pd.read_csv(file_path, chunksize=500_000):
        chunks.append(chunk)
    df = pd.concat(chunks, ignore_index=True)

    summary = df.groupby("platform").agg(
        spend=("spend", "sum"),
        revenue=("revenue", "sum"),
        clicks=("clicks", "sum"),
        impressions=("impressions", "sum"),
        conversions=("conversions", "sum"),
    ).reset_index()

    summary["ROAS"] = summary["revenue"] / summary["spend"]
    summary["CTR"]  = summary["clicks"] / summary["impressions"]
    summary["CPA"]  = summary["spend"] / summary["conversions"]

    # ROAS ke hisaab se budget allocate karo
    summary["weight"] = summary["ROAS"] / summary["ROAS"].sum()
    summary["allocated_budget"] = (summary["weight"] * total_budget).round(0)
    summary["expected_revenue"] = (summary["allocated_budget"] * summary["ROAS"]).round(0)
    summary["expected_profit"]  = summary["expected_revenue"] - summary["allocated_budget"]

    summary = summary.sort_values("ROAS", ascending=False)

    print("\n💡 RECOMMENDED BUDGET ALLOCATION:")
    for _, row in summary.iterrows():
        pct = (row["allocated_budget"] / total_budget) * 100
        print(f"   {row['platform']:<10} → Rs. {int(row['allocated_budget']):>8,}  ({pct:4.1f}%)  | Est. Profit: Rs. {int(row['expected_profit']):>10,}")

    total_rev = summary["expected_revenue"].sum()
    total_profit = summary["expected_profit"].sum()
    
    print(f"\n📈 TOTAL EXPECTED REVENUE:  Rs. {int(total_rev):,}")
    print(f"📈 TOTAL EXPECTED PROFIT:   Rs. {int(total_profit):,}")
    print(f"✅ Recommendation complete!\n")

if __name__ == "__main__":
    file = "data/ads_1m.csv"
    if os.path.exists(file):
        recommend_budget(file, total_budget=1_000_000)
    else:
        print("File nahi mili, pehle data_generator.py chalayein.")