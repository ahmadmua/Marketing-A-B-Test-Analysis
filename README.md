# Marketing A/B Test Analysis

An end-to-end statistical analysis of a real-world marketing A/B test, examining whether ad exposure drives significantly higher conversion rates compared to public service announcements (PSA). The project covers data exploration, hypothesis testing, effect size estimation, and a Power BI dashboard.

---

## Dashboard

A Power BI dashboard summarizes all findings in a single view, including KPI cards, the frequency effect chart, day-of-week and hour-of-day breakdowns, and a statistical summary panel.

<img width="1427" height="814" alt="image" src="https://github.com/user-attachments/assets/53b6dc4f-38bd-4683-b0de-4dea6455cd85" />

---

## Dataset

**Source:** [Marketing A/B Testing Dataset](https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing) — Kaggle  
**Size:** ~588,000 rows  
**Features:**

| Column | Description |
|---|---|
| `test group` | Whether the user saw an `ad` or a `psa` |
| `converted` | Whether the user converted (True/False) |
| `total ads` | Number of ads seen by the user |
| `most ads day` | Day of week with highest ad exposure |
| `most ads hour` | Hour of day with highest ad exposure |

---

## SQL Queries

- Sanity check: row count + group split
- Core conversion rates by group
- Conversion rate by ad exposure frequency (segmentation)
- Day-of-week pattern (the days users most often saw the ad)
- Hour-of-day pattern
---

## Methodology

### 1. Chi-Square Test of Independence
Tests whether conversion rate differs significantly between the ad and PSA groups.

- **Null hypothesis (H₀):** Conversion rate is independent of group assignment
- **Test:** Chi-square (2×2 contingency table)
- **Result:** χ²(1) = 54.01, p < 0.001 → **Reject H₀**

> **Note on p-value underflow:** With ~589K observations, the true p-value is approximately 2e-13 — far below Python's float precision floor (~5e-324), causing it to display as `0.0`. The result is reported as `< 0.001` throughout.

### 2. Effect Size — Relative & Absolute Lift
Statistical significance alone doesn't indicate practical importance. Lift metrics quantify the real-world magnitude of the effect.

- **Absolute lift:** Difference in raw conversion rates
- **Relative lift:** Percentage improvement of ad group over PSA baseline

### 3. 95% Confidence Intervals
Wilson-style proportion CIs confirm that the observed difference is not attributable to sampling noise, and that the two group intervals do not overlap.

### 4. Mann-Whitney U Test
A non-parametric test examining whether converted users were exposed to significantly more ads than non-converted users — isolating the frequency dimension of ad effectiveness.

---

## Key Findings

| Metric | Value |
|---|---|
| Ad conversion rate | **2.55%** |
| PSA conversion rate | **1.79%** |
| Absolute lift | **+0.77 pp** |
| Relative lift | **+43.1%** |
| Chi-square statistic | **54.01** |
| Degrees of freedom | **1** |
| p-value | **< 0.001** |
| Decision | **Reject H₀** |

### Ad Frequency Effect
Conversion rate increases sharply with ad exposure frequency. Users who saw **100+ ads** converted at ~17% — roughly 10× the baseline rate. This is the single strongest signal in the dataset and suggests a clear dose-response relationship between ad frequency and purchase intent.

| Frequency Bucket | Approx. Conversion Rate |
|---|---|
| 1–5 ads | ~1% |
| 6–15 ads | ~1.5% |
| 16–30 ads | ~2% |
| 31–60 ads | ~4% |
| 61–100 ads | ~10% |
| 100+ ads | ~17% |

### Temporal Patterns
- **Day of week:** Monday and Tuesday show the highest conversion rates; Saturday the lowest — suggesting weekday audiences are more purchase-intent driven
- **Hour of day:** Conversions peak in the late evening (hours 20–22), with a trough in the early morning (hours 2–5)

### Group Size Imbalance
The ad group (565K users) is significantly larger than the PSA group (24K users). While the chi-square test accounts for this, the PSA baseline conversion rate should be interpreted with more caution given the smaller sample.

---

## Tools Used

- **Python** — pandas, scipy, numpy (statistical testing)
- **Power BI** — DAX measures, interactive dashboard
- **Dataset** — Kaggle (public domain)

---

## Project Structure

```
├── analysis.py        # Statistical tests and output
├── marketing_AB.csv   # dataset
├── ab_test.pbix       # Power BI dashboard export
├── AB_Test.sql        # SQL Queries for analysis
└── README.md
```

---

## Insights & Recommendations

**1. Frequency is the real lever** — ads outperform PSAs, but users who saw 100+ ads converted at ~17% vs ~1% for low-exposure users.

**2. Optimal delivery window** — Monday/Tuesday evenings (8–10 PM) show the highest conversion rates. Concentrating ad spend here should improve efficiency.

**3. Statistical vs. business significance** — the p-value is overwhelming, but the absolute lift is only 0.77 pp. Whether ads justify the cost over PSAs requires revenue-per-conversion and CPM data — this analysis answers *whether* ads work, not *whether they're worth it*.

**4. Frequency cap risk** — the 100+ bucket likely reflects self-selected high-intent users, not a causal case for flooding everyone with ads. Ad fatigue isn't captured here.

---
