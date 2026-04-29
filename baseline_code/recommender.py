import pandas as pd

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

ingredient_groups = {k: v for k, v in df.groupby("ing_norm")}
brand_list = df["brand_norm"].tolist()

def simple_similarity(a, b):
    if not a or not b:
        return 0
    set_a = set(a)
    set_b = set(b)
    return int(100 * len(set_a & set_b) / len(set_a | set_b))

def extract_best_match(query):
    best_score = -1
    best_idx = -1

    for i, brand in enumerate(brand_list):
        score = simple_similarity(query, brand)
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
    base_strength = base["strength_norm"]
    base_dosage = base["dosage_norm"]
    base_brand = base["brand_norm"]

    potential = ingredient_groups.get(base_ing)
    if potential is None or len(potential) <= 1:
        return pd.DataFrame()

    best_score = -1
    best_row = None

    for _, row in potential.iterrows():
        if row["brand_norm"] == base_brand:
            continue

        # Fast scoring
        s_match = simple_similarity(row["strength_norm"], base_strength)
        d_match = 100 if row["dosage_norm"] == base_dosage else 0

        score = (s_match * 0.7) + (d_match * 0.3)

        # 🔥 EARLY EXIT (perfect match)
        if score == 100:
            return pd.DataFrame([row[[
                "brand_name", "primary_ingredient",
                "primary_strength", "dosage_form"
            ]]])

        if score > best_score:
            best_score = score
            best_row = row

    if best_row is None:
        return pd.DataFrame()

    return pd.DataFrame([best_row[[
        "brand_name", "primary_ingredient",
        "primary_strength", "dosage_form"
    ]]])
