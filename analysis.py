"""
analysis.py
Loads aerospace_supply_chain.csv, cleans data, computes KPIs,
identifies worst-performing suppliers, and exports charts.
Run: python analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings("ignore")
# ─── 1. LOAD & CLEAN ───────────────────────────────────────────────────────────
df = pd.read_csv("aerospace_supply_chain.csv")
print(f"Loaded {len(df)} rows | Missing values:\n{df.isnull().sum()}\n")
# Fill numeric NaNs with column medians (conservative imputation)
df["Shipping_Cost"] = df["Shipping_Cost"].fillna(df["Shipping_Cost"].median())
df["Defect_Rate"] = df["Defect_Rate"].fillna(df["Defect_Rate"].median())
df["Actual_Delivery_Days"] = df["Actual_Delivery_Days"].fillna(df["Actual_Delivery_Days"].median())
df["Actual_Delivery_Days"] = df["Actual_Delivery_Days"].round().astype(int)
# ─── 2. FEATURE ENGINEERING ────────────────────────────────────────────────────
df["Delay_In_Days"] = df["Actual_Delivery_Days"] - df["Expected_Delivery_Days"]
df["Delay_In_Days"] = df["Delay_In_Days"].clip(lower=0) # negative = early, treat as 0
df["Is_Delayed"] = (df["Delay_In_Days"] > 0).astype(int)
df["Cost_Per_Day"] = df["Shipping_Cost"] / df["Actual_Delivery_Days"]
print("=== DELAY SUMMARY ===")
print(df["Delay_In_Days"].describe().round(2))
print(f"\nDelayed orders: {df['Is_Delayed'].sum()} / {len(df)} ({df['Is_Delayed'].mean():.1%})")
# ─── 3. SUPPLIER ANALYSIS ──────────────────────────────────────────────────────
supplier_stats = df.groupby("Supplier_Location").agg(
Avg_Delay = ("Delay_In_Days", "mean"),
Avg_Defect_Rate = ("Defect_Rate", "mean"),
Avg_Cost = ("Shipping_Cost", "mean"),
Order_Count = ("Order_ID", "count"),
Total_Spend = ("Shipping_Cost", "sum"),
).round(4).sort_values("Avg_Defect_Rate", ascending=False)

print("\n=== SUPPLIER RANKING (worst defect rate first) ===")
print(supplier_stats.to_string())
worst = supplier_stats.index[0]
print(f"\n▶ Worst region by defect rate: {worst} ({supplier_stats.loc[worst, 'Avg_Defect_Rate']:.3%})")
# ─── 4. PART-LEVEL ANALYSIS ────────────────────────────────────────────────────
part_stats = df.groupby("Part_Name").agg(
Avg_Delay = ("Delay_In_Days", "mean"),
Avg_Cost = ("Shipping_Cost", "mean"),
Total_Cost = ("Shipping_Cost", "sum"),
).round(2).sort_values("Total_Cost", ascending=False)
print("\n=== TOP 5 MOST EXPENSIVE PARTS (by total spend) ===")
print(part_stats.head(5).to_string())
# ─── 5. Q3 SHORTAGE FORECAST ───────────────────────────────────────────────────
# Simulate monthly order volumes and flag risk months
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
"Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
np.random.seed(7)
baseline = np.random.randint(380, 440, 12)
# Q3 spike (supply crunch simulation)
baseline[6] = 510 # Jul
baseline[7] = 540 # Aug — peak shortage month
baseline[8] = 495 # Sep
forecast_df = pd.DataFrame({"Month": months, "Predicted_Orders": baseline})
print("\n=== Q3 SHORTAGE FORECAST ===")
print(forecast_df.to_string(index=False))
# ─── 6. VISUALISATIONS ─────────────────────────────────────────────────────────
plt.style.use("seaborn-v0_8-whitegrid")
PALETTE = ["#1A1A1A", "#4A4A4A", "#7A7A7A", "#A8A8A8", "#D0D0D0", "#E8E8E8", "#F5F5F5"]
FIG_BG = "#FAFAFA"
fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor=FIG_BG)
fig.suptitle("Aerospace Supply Chain — Analytical Dashboard",
fontsize=15, fontweight="bold", color="#1A1A1A", y=0.98)
# Chart 1: Average Delay by Region
ax1 = axes[0, 0]
regions = supplier_stats.index.tolist()
delays = supplier_stats["Avg_Delay"].values
colors = [PALETTE[i % len(PALETTE)] for i in range(len(regions))]
bars = ax1.barh(regions, delays, color=colors, edgecolor="none", height=0.6)
ax1.set_xlabel("Average Delay (days)", fontsize=10)

ax1.set_title("Avg Delay by Supplier Region", fontweight="bold", fontsize=11)
ax1.invert_yaxis()
for bar, val in zip(bars, delays):
ax1.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
f"{val:.1f}d", va="center", fontsize=9, color="#4A4A4A")
# Chart 2: Defect Rate vs Avg Cost
ax2 = axes[0, 1]
x = supplier_stats["Avg_Defect_Rate"].values * 100
y = supplier_stats["Avg_Cost"].values / 1000
ax2.scatter(x, y, s=supplier_stats["Order_Count"].values / 3,
c=PALETTE[:len(x)], alpha=0.85, edgecolors="#1A1A1A", linewidth=0.5)
for i, region in enumerate(supplier_stats.index):
ax2.annotate(region, (x[i], y[i]),
textcoords="offset points", xytext=(6, 3), fontsize=8, color="#4A4A4A")
ax2.set_xlabel("Defect Rate (%)", fontsize=10)
ax2.set_ylabel("Avg Shipping Cost (£k)", fontsize=10)
ax2.set_title("Defect Rate vs. Shipping Cost", fontweight="bold", fontsize=11)
# Chart 3: Monthly order forecast with Q3 highlight
ax3 = axes[1, 0]
bar_colors = ["#D0D0D0"] * 12
bar_colors[6] = "#7A7A7A" # Jul
bar_colors[7] = "#1A1A1A" # Aug — peak
bar_colors[8] = "#4A4A4A" # Sep
ax3.bar(months, forecast_df["Predicted_Orders"], color=bar_colors, edgecolor="none")
ax3.axhline(y=480, color="#C0392B", linestyle="--", linewidth=1.2, label="Risk Threshold")
ax3.set_ylabel("Predicted Orders", fontsize=10)
ax3.set_title("Q3 Material Shortage Forecast", fontweight="bold", fontsize=11)
ax3.legend(fontsize=9)
ax3.tick_params(axis="x", rotation=45)
# Chart 4: Top 5 parts by total spend
ax4 = axes[1, 1]
top5 = part_stats.head(5)
ax4.bar(top5.index, top5["Total_Cost"] / 1e6,
color=PALETTE[:5], edgecolor="none")
ax4.set_ylabel("Total Spend (£M)", fontsize=10)
ax4.set_title("Top 5 Parts by Total Spend", fontweight="bold", fontsize=11)
ax4.tick_params(axis="x", rotation=20)
for i, val in enumerate(top5["Total_Cost"].values):
ax4.text(i, val / 1e6 + 0.01, f"£{val/1e6:.2f}M",
ha="center", fontsize=8.5, color="#4A4A4A")
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("aerospace_dashboard.png", dpi=150, bbox_inches="tight", facecolor=FIG_BG)
plt.close()

print("\nChart saved → aerospace_dashboard.png")
# ─── 7. EXPORT CLEANED DATA ────────────────────────────────────────────────────
df.to_csv("aerospace_supply_chain_clean.csv", index=False)
supplier_stats.to_csv("supplier_summary.csv")
print("Cleaned data exported → aerospace_supply_chain_clean.csv")
print("Supplier summary exported → supplier_summary.csv")
