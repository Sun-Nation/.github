"""
Finca Duna — Commodity vs Specialty green coffee price trend (5 years).

Commodity line: ICO Composite Indicator Price (I-CIP), calendar-year avg, US$/lb.
  Source: International Coffee Organization monthly market reports.
  2023 & 2024 confirmed; 2021, 2022, 2025 reconstructed/approx from ICO monthly data.

Specialty line: median FOB green price from the Specialty Coffee Transaction Guide,
  mapped from crop year to its later calendar year (e.g. 2024/25 -> 2025), US$/lb.
  Source: Specialty Coffee Transaction Guide (2021-2025 editions).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

years = [2021, 2022, 2023, 2024, 2025]

# Commodity baseline — ICO I-CIP calendar-year average ($/lb)
commodity = [1.51, 1.79, 1.65, 2.29, 3.10]

# Specialty median FOB green ($/lb), crop year mapped to later calendar year
# 2020/21->2021, 2021/22->2022, 2022/23->2023, 2023/24->2024, 2024/25->2025
specialty = [2.00, 3.50, 3.40, 3.50, 4.39]

# Specialty 25th-75th percentile band is only published for the latest year (2024/25)
spec_lo_2025, spec_hi_2025 = 3.70, 5.50

# High-score / top-tier line (88+). SPARSE, MIXED-BASIS DATA - only anchors we can defend:
#   2022 (2021/22): $5.11  = median for cup 88+ (solid)
#   2023 (2022/23): $4.91  = 87-pt, 1,000-lb lot (proxy for high tier)
#   2025 (2024/25): $5.50  = 75th-percentile of all specialty (high-score proxy, solid)
# 2021 and 2024 omitted - no defensible 88+ figure found in accessible sources.
topyears = [2022, 2023, 2025]
toptier = [5.11, 4.91, 5.50]

fig, ax = plt.subplots(figsize=(10, 6))

# Shade the premium (gap) between specialty and commodity
ax.fill_between(years, commodity, specialty, color="#4caf50", alpha=0.12,
                label="Specialty premium (gap)")

# Commodity line
ax.plot(years, commodity, marker="o", linewidth=2.5, color="#8d6e63",
        label="Commodity (ICO I-CIP, calendar-yr avg)")
# Specialty line
ax.plot(years, specialty, marker="o", linewidth=2.5, color="#2e7d32",
        label="Specialty median (FOB green, Transaction Guide)")
# High-score / top-tier line (dashed, open markers = sparse/mixed-basis data)
ax.plot(topyears, toptier, marker="^", markerfacecolor="white", linestyle="--",
        linewidth=2.0, color="#1b5e20",
        label="Top tier 88+ / 75th-pct (sparse, mixed-basis)")
for x, y in zip(topyears, toptier):
    ax.annotate(f"${y:.2f}", (x, y), textcoords="offset points",
                xytext=(0, 9), ha="center", fontsize=8, color="#1b5e20",
                fontweight="bold")

# Latest-year specialty 25-75 percentile range as a vertical whisker
ax.plot([2025, 2025], [spec_lo_2025, spec_hi_2025], color="#2e7d32",
        linewidth=1.2, alpha=0.7)
ax.plot([2024.95, 2025.05], [spec_hi_2025, spec_hi_2025], color="#2e7d32", alpha=0.7)
ax.plot([2024.95, 2025.05], [spec_lo_2025, spec_lo_2025], color="#2e7d32", alpha=0.7)
ax.annotate("2024/25 specialty\n25th-75th pct\n$3.70-$5.50",
            xy=(2025, spec_hi_2025), xytext=(2024.45, 5.35),
            fontsize=8, color="#2e7d32")

# Data labels
for x, y in zip(years, commodity):
    ax.annotate(f"${y:.2f}", (x, y), textcoords="offset points",
                xytext=(0, -16), ha="center", fontsize=8, color="#5d4037")
for x, y in zip(years, specialty):
    ax.annotate(f"${y:.2f}", (x, y), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=8, color="#1b5e20")

# Premium callouts
for x, c, s in zip(years, commodity, specialty):
    prem = s - c
    ax.annotate(f"+${prem:.2f}", (x, (c + s) / 2), ha="center",
                fontsize=7.5, color="#388e3c", style="italic")

ax.set_title("Green Coffee Prices: Commodity vs Specialty (2021-2025)",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("US$ per pound (green / FOB)")
ax.set_xticks(years)
ax.set_ylim(0, 6)
ax.grid(True, alpha=0.25)
ax.legend(loc="upper left", fontsize=9)

fig.text(0.5, 0.01,
         "Sources: ICO Composite Indicator Price (monthly reports) · "
         "Specialty Coffee Transaction Guide (2021-2025). "
         "Specialty crop years mapped to later calendar year; some commodity figures approx.",
         ha="center", fontsize=6.5, color="gray")

fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig("FINCA-DUNA/coffee-price-trend.png", dpi=150)
print("saved FINCA-DUNA/coffee-price-trend.png")
