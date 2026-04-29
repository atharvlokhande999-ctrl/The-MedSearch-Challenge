
import pandas as pd
from rapidfuzz import fuzz, process

# ----------------------------
# LOAD + PREPROCESS (ONE TIME)
# ----------------------------
df = pd.read_csv("baseline_code/Medsearch_Data.csv")

df.columns = df.columns.str.strip()

def normalize(text):
    if pd.isna(text):
        return ""
    return str(text).strip().lower()

# Precompute normalized columns (vectorized)
df["brand_norm"] = df["brand_name"].astype(str).str.strip().str.lower()
df["ing_norm"] = df["primary_ingredient"].astype(str).str.strip().str.lower()
df["strength_norm"] = df["primary_strength"].astype(str).str.replace(" ", "").str.lower()
df["dosage_norm"] = df["dosage_form"].astype(str).str.strip().str.lower()

# Convert to numpy arrays (FASTER access)
brand_array = df["brand_norm"].values

# ----------------------------
# MAIN FUNCTION (OPTIMIZED)
# ----------------------------
def recommend_alternatives(query, top_k=5):
    if not query:
        return pd.DataFrame()

    query_norm = query.strip().lower()

    # ⚡ FASTEST MATCH (no full loop)
    match = process.extractOne(query_norm, brand_array, scorer=fuzz.WRatio)

    if not match or match[1] < 60:
        return pd.DataFrame()

    idx = match[2]
    base = df.iloc[idx]

    base_ing = base["ing_norm"]
    base_strength = base["strength_norm"]
    base_dosage = base["dosage_norm"]
    base_brand = base["brand_norm"]

    # ⚡ FILTER FIRST (huge speed gain)
    mask = (df["ing_norm"].values == base_ing)
    potential_idx = mask.nonzero()[0]

    if len(potential_idx) <= 1:
        return pd.DataFrame()

    subset = df.iloc[potential_idx]

    # ⚡ VECTORIZE STRENGTH SIMILARITY
    strength_scores = [
        fuzz.ratio(s, base_strength)
        for s in subset["strength_norm"].values
    ]

    # ⚡ VECTORIZE DOSAGE MATCH
    dosage_scores = (subset["dosage_norm"].values == base_dosage) * 100

    # ⚡ FINAL SCORE (NUMPY FAST)
    final_scores = (0.7 * pd.Series(strength_scores).values +
                    0.3 * dosage_scores)

    subset = subset.copy()
    subset["final_score"] = final_scores

    # ⚡ REMOVE SAME BRAND (vectorized)
    subset = subset[subset["brand_norm"].values != base_brand]

    # ⚡ FAST SORT (nlargest faster than sort_values)
    result = subset.nlargest(top_k, "final_score")

    return result[
        ["brand_name", "primary_ingredient", "primary_strength", "dosage_form"]
    ]
