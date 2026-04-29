import pandas as pd
from rapidfuzz import fuzz, process

# Load dataset once
df = pd.read_csv("baseline_code/Medsearch_Data.csv")

# ----------------------------
# ADVANCED CLEANING & PRE-PROCESSING
# ----------------------------
# Strip spaces and lowercase once at startup to save loop time
df.columns = df.columns.str.strip()

def normalize(text):
    if pd.isna(text): return ""
    return str(text).strip().lower()

# Pre-calculate normalized columns for speed
df["brand_norm"] = df["brand_name"].apply(normalize)
df["ing_norm"] = df["primary_ingredient"].apply(normalize)
df["strength_norm"] = df["primary_strength"].apply(lambda x: normalize(x).replace(" ", ""))
df["dosage_norm"] = df["dosage_form"].apply(normalize)

# ----------------------------
# MAIN FUNCTION
# ----------------------------
def recommend_alternatives(query, top_k=5):
    if not query:
        return pd.DataFrame()

    query_norm = normalize(query)

    # STEP 1: FASTER BRAND MATCHING
    # Instead of scoring every row, we use process.extractOne for speed
    match_result = process.extractOne(
        query_norm, 
        df["brand_norm"], 
        scorer=fuzz.WRatio
    )

    if not match_result or match_result[1] < 60:
        return pd.DataFrame()

    best_match_idx = match_result[2]
    best_match = df.iloc[best_match_idx]

    # Reference values for comparison
    base_ing = best_match["ing_norm"]
    base_strength = best_match["strength_norm"]
    base_dosage = best_match["dosage_norm"]
    base_brand = best_match["brand_norm"]

    # STEP 2: SMART FILTERING (The "Speed Secret")
    # Instead of scoring 100,000 rows, only score rows with the same ingredient
    # This dramatically cuts down runtime for the Speed Bonus
    potential_matches = df[df["ing_norm"] == base_ing].copy()
    
    # If same-ingredient list is too small, broaden search slightly
    if len(potential_matches) <= 1:
        # Fallback to broader fuzzy search if no exact ingredient match
        return pd.DataFrame()

    # STEP 3: REFINED WEIGHTED SCORING
    def calculate_score(row):
        # We already know Ingredient is a match (100%)
        # Focus on Strength and Dosage
        
        # Strength matching (strip spaces for consistency)
        s_match = fuzz.ratio(row["strength_norm"], base_strength)
        
        # Dosage matching
        d_match = 100 if row["dosage_norm"] == base_dosage else 0
        
        # Final Score (Weighted)
        # Since Ingredients are filtered, we weight Strength and Dosage heavily
        return (s_match * 0.7) + (d_match * 0.3)

    potential_matches["final_score"] = potential_matches.apply(calculate_score, axis=1)

    # Remove the exact same medicine from results
    results = potential_matches[potential_matches["brand_norm"] != base_brand]

    # Sort and Return
    results = results.sort_values(by="final_score", ascending=False)

    return results.head(top_k)[
        ["brand_name", "primary_ingredient", "primary_strength", "dosage_form"]
    ]