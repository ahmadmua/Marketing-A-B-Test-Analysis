import pandas as pd
from scipy import stats
from scipy.stats import chi2_contingency, mannwhitneyu
import numpy as np

df = pd.read_csv("marketing_AB.csv")

# --- Chi-Square Test (primary: conversion rate difference) ---
ad  = df[df["test group"] == "ad"]
psa = df[df["test group"] == "psa"]

contingency = pd.crosstab(df["test group"], df["converted"])
chi2, p_value, dof, expected = chi2_contingency(contingency)

print(f"Chi-square: {chi2:.2f}, p-value: {p_value:.6f}")
# If p < 0.05 → statistically significant

# --- Effect size: Relative lift ---
rate_ad  = ad["converted"].mean()
rate_psa = psa["converted"].mean()
lift = (rate_ad - rate_psa) / rate_psa * 100
print(f"Ad conversion: {rate_ad:.4f}, PSA: {rate_psa:.4f}, Lift: {lift:.1f}%")

# --- Practical significance: 95% Confidence Intervals ---
def proportion_ci(successes, n, z=1.96):
    p = successes / n
    margin = z * np.sqrt(p * (1 - p) / n)
    return p - margin, p + margin

ci_ad  = proportion_ci(ad["converted"].sum(), len(ad))
ci_psa = proportion_ci(psa["converted"].sum(), len(psa))
print(f"Ad CI:  {ci_ad}\nPSA CI: {ci_psa}")

# Tests whether converted users saw significantly more ads
converted     = df[df["converted"] == True]["total ads"]
not_converted = df[df["converted"] == False]["total ads"]
u_stat, p_mw = mannwhitneyu(converted, not_converted, alternative="greater")
p_display = p_value if p_value > 0 else "< 1e-300"
print(f"Chi-square: {chi2:.2f}, p-value: {p_display}")