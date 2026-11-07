# 💰 Digital Advertising Budget Optimizer

## 🎯 Industry Problem
A company spends *Rs. 1 million/month* across Facebook, Instagram, Google, TikTok, and YouTube. 
*Where should the budget go to maximize profit?*

## 🛠️ Solution
A complete data pipeline that:
1. Simulates realistic ad-campaign data (10K → 10M rows)
2. Computes *CTR, CPC, CPA, CVR, ROAS*
3. Compares *Pandas vs Spark* for scalability
4. Recommends optimal budget allocation based on historical ROAS

## 📊 Metrics Used
| Metric | Formula |
|--------|---------|
| CTR | clicks / impressions |
| CPC | spend / clicks |
| CPA | spend / conversions |
| CVR | conversions / clicks |
| ROAS | revenue / spend |

## 📈 Results (Sample on 1M Rows)
| Platform | ROAS | Recommended Budget (Rs. 1M) | Est. Profit |
|----------|------|----------------------------|-------------|
| YouTube | 6.18 | Rs. 250,945 (25.1%) | Rs. 1,301,814 |
| Google | 5.94 | Rs. 241,200 (24.1%) | Rs. 1,193,304 |
| Facebook | 5.48 | Rs. 222,482 (22.2%) | Rs. 998,015 |
| Instagram | 3.70 | Rs. 150,340 (15.0%) | Rs. 406,968 |
| TikTok | 3.33 | Rs. 135,032 (13.5%) | Rs. 314,562 |
| *Total* | | *Rs. 1,000,000* | *Rs. 4,214,663* |

## 🚀 How to Run
```bash
pip install -r requirements.txt
python data_generator.py      # Generates 10K to 10M rows data
python data/metrics_pandas.py # Pandas analysis
python data/budget_optimizer.py # Final budget recommendation
## 🏗️ Tech Stack
* Python
* Pandas (for small to medium data)
* PySpark (for Big Data scalability)
* NumPy & Faker (for data simulation)

## 👤 Author
**Houria Khan** 
[GitHub Profile](https://github.com/hourianarana)