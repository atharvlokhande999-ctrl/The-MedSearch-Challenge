import pandas as pd
import numpy as np
from rapidfuzz import fuzz, process

df = pd.read_csv("baseline_code/Medsearch_Data.csv")

df.columns = df.columns.str.strip()

def normalize(text):
    if pd.isna(text):
        return ""
    return str(text).strip().lower()

df["brand_norm"] = df["brand_name"].map(normalize)
df["ing_norm"] = df["primary_ingredient"].map(normalize)
df["strength_norm"] = df["primary_strength"].map(lambda x: normalize(x).replace(" ", ""))
df["dosage_norm"] = df["dosage_form"].map(normalize)

# 🔥 Pre-group for O(1) lookup
ingredient_groups = {k: v for k, v in df.groupby("ing_norm")}

brand_list = df["brand_norm"].tolist()

def recommend_alternatives(query, top_k=5):
    if not query:
        return pd.DataFrame()

    query_norm = normalize(query)

    match = process.extractOne(query_norm, brand_list, scorer=fuzz.QRatio)

    if not match or match[1] < 60:
        return pd.DataFrame()

    idx = match[2]
    base = df.iloc[idx]

    base_ing = base["ing_norm"]
    base_strength = base["strength_norm"]
    base_dosage = base["dosage_norm"]
    base_brand = base["brand_norm"]

    if base_ing not in ingredient_groups:
        return pd.DataFrame()

    potential = ingredient_groups[base_ing]

    if len(potential) <= 1:
        return pd.DataFrame()

    # 🔥 Vectorized scoring
    strength_scores = potential["strength_norm"].map(
        lambda x: fuzz.ratio(x, base_strength)
    ).values

    dosage_scores = (potential["dosage_norm"].values == base_dosage).astype(int) * 100

    final_scores = (strength_scores * 0.7) + (dosage_scores * 0.3)

    potential = potential.assign(final_score=final_scores)

    results = potential[potential["brand_norm"] != base_brand]

    return results.nlargest(top_k, "final_score")[
        ["brand_name", "primary_ingredient", "primary_strength", "dosage_form"]
    ]
