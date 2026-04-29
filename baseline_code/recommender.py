# Importing 
import pandas as pd
import numpy as np

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

# 🔥 Precompute sets (BIG SPEED BOOST)
df["strength_set"] = df["strength_norm"].map(set)
df["brand_set"] = df["brand_norm"].map(set)

ingredient_groups = {k: v for k, v in df.groupby("ing_norm")}

brand_list = df["brand_norm"].tolist()
brand_sets = df["brand_set"].tolist()

def fast_similarity(set_a, set_b):
    if not set_a or not set_b:
        return 0
    return int(100 * len(set_a & set_b) / len(set_a | set_b))

def extract_best_match(query):
    q_set = set(query)

    best_score = -1
    best_idx = -1

    for i in range(len(brand_list)):
        score = fast_similarity(q_set, brand_sets[i])
        if score > best_score:
            best_score = score
            best_idx = i

    return best_idx, best_score


def recommend_alternatives(query):
    if not query:
        return pd.DataFrame()

    query_norm = normalize(query)

    idx, score = extract_best_match(query_norm)
    if score < 40:
        return pd.DataFrame()

    base = df.iloc[idx]

    base_ing = base["ing_norm"]
    base_strength_set = base["strength_set"]
    base_dosage = base["dosage_norm"]
    base_brand = base["brand_norm"]

    potential = ingredient_groups.get(base_ing)
    if potential is None or len(potential) <= 1:
        return pd.DataFrame()

    # Convert to arrays for speed
    strength_sets = potential["strength_set"].values
    dosage_arr = potential["dosage_norm"].values
    brand_arr = potential["brand_norm"].values

    best_score = -1
    best_idx = -1

    for i in range(len(potential)):
        if brand_arr[i] == base_brand:
            continue

        s_match = fast_similarity(strength_sets[i], base_strength_set)
        d_match = 100 if dosage_arr[i] == base_dosage else 0

        score = (s_match * 0.7) + (d_match * 0.3)

        if score == 100:
            best_idx = i
            break

        if score > best_score:
            best_score = score
            best_idx = i

    if best_idx == -1:
        return pd.DataFrame()

    row = potential.iloc[best_idx]

    return pd.DataFrame([row[[
        "brand_name",
        "primary_ingredient",
        "primary_strength",
        "dosage_form"
    ]]])
    
