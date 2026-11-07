import pandas as pd
import numpy as np
from faker import Faker
import os

fake = Faker()

# Platform-wise realistic performance (real duniya jaisa)
PLATFORM_PROFILES = {
    "Facebook":  {"ctr": 0.018, "cvr": 0.045, "cpc": 12.0, "aov": 1500},
    "Instagram": {"ctr": 0.022, "cvr": 0.038, "cpc": 14.0, "aov": 1400},
    "Google":    {"ctr": 0.035, "cvr": 0.060, "cpc": 18.0, "aov": 1800},
    "TikTok":    {"ctr": 0.025, "cvr": 0.025, "cpc": 8.0,  "aov": 1100},
    "YouTube":   {"ctr": 0.015, "cvr": 0.040, "cpc": 10.0, "aov": 1600},
}

CAMPAIGNS = ["Summer_Sale", "Festive_Offer", "Brand_Awareness", "Retargeting", "New_Launch"]
DEVICES = ["Mobile", "Desktop", "Tablet"]
GENDERS = ["Male", "Female", "Other"]
CITIES = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", "Peshawar", "Quetta"]


def generate_data(n_rows, output_path):
    """n_rows jitne records banao aur CSV mein save karo"""
    print(f"Generating {n_rows:,} rows...")

    platforms = np.random.choice(list(PLATFORM_PROFILES.keys()), size=n_rows)
    campaigns = np.random.choice(CAMPAIGNS, size=n_rows)
    devices = np.random.choice(DEVICES, size=n_rows, p=[0.65, 0.25, 0.10])
    genders = np.random.choice(GENDERS, size=n_rows, p=[0.55, 0.43, 0.02])
    cities = np.random.choice(CITIES, size=n_rows)
    ages = np.random.randint(18, 65, size=n_rows)

    # Har platform ke profile ke hisaab se metrics
    impressions = np.random.randint(500, 50000, size=n_rows)
    ctr_arr = np.array([PLATFORM_PROFILES[p]["ctr"] for p in platforms])
    clicks = np.maximum(1, (impressions * ctr_arr * np.random.uniform(0.7, 1.3, n_rows)).astype(int))

    cpc_arr = np.array([PLATFORM_PROFILES[p]["cpc"] for p in platforms])
    spend = np.round(clicks * cpc_arr * np.random.uniform(0.8, 1.2, n_rows), 2)

    cvr_arr = np.array([PLATFORM_PROFILES[p]["cvr"] for p in platforms])
    conversions = np.maximum(0, (clicks * cvr_arr * np.random.uniform(0.7, 1.3, n_rows)).astype(int))

    aov_arr = np.array([PLATFORM_PROFILES[p]["aov"] for p in platforms])
    revenue = np.round(conversions * aov_arr * np.random.uniform(0.85, 1.15, n_rows), 2)

    dates = pd.date_range("2024-01-01", periods=365, freq="D")
    date_col = np.random.choice(dates, size=n_rows)

    df = pd.DataFrame({
        "date": date_col,
        "campaign": campaigns,
        "platform": platforms,
        "impressions": impressions,
        "clicks": clicks,
        "spend": spend,
        "conversions": conversions,
        "revenue": revenue,
        "age": ages,
        "gender": genders,
        "city": cities,
        "device": devices,
    })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Saved: {output_path}  |  Shape: {df.shape}\n")
    return df


if __name__ == "__main__":
    levels = {
        10_000:     "data/ads_10k.csv",
        100_000:    "data/ads_100k.csv",
        1_000_000:  "data/ads_1m.csv",
        10_000_000: "data/ads_10m.csv",
    }
    for n, path in levels.items():
        generate_data(n, path)
    print("🎉 Saara data generate ho gaya!")