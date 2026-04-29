import pandas as pd
import time
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from baseline_code.recommender import recommend_alternatives
from hidden_evaluation.scoring import calculate_final_score

# Load hidden files
hidden_tests = pd.read_csv("hidden_evaluation/hidden_test_data.csv")
benchmarks = pd.read_csv("hidden_evaluation/benchmark_answers.csv")

# ✅ Faster lookup (O(1) instead of filtering each loop)
benchmark_map = benchmarks.set_index("brand_name").to_dict("index")

results = []

for _, row in hidden_tests.iterrows():
    query = row["brand_name"]

    start = time.perf_counter()

    try:
        output = recommend_alternatives(query)
        runtime = time.perf_counter() - start

        # ✅ Safe checks
        benchmark = benchmark_map.get(query)

        if benchmark is None or output is None or getattr(output, "empty", True):
            results.append({
                "query": query,
                "ingredient_match": False,
                "strength_match": False,
                "dosage_match": False,
                "returned_output": False,
                "runtime": runtime
            })
            continue

        # Top recommendation
        top_result = output.iloc[0]

        ingredient_match = (
            str(top_result.get("primary_ingredient", "")).strip().lower()
            ==
            str(benchmark.get("expected_primary_ingredient", "")).strip().lower()
        )

        strength_match = (
            str(top_result.get("primary_strength", "")).strip().lower()
            ==
            str(benchmark.get("expected_primary_strength", "")).strip().lower()
        )

        dosage_match = (
            str(top_result.get("dosage_form", "")).strip().lower()
            ==
            str(benchmark.get("expected_dosage_form", "")).strip().lower()
        )

        results.append({
            "query": query,
            "ingredient_match": ingredient_match,
            "strength_match": strength_match,
            "dosage_match": dosage_match,
            "returned_output": True,
            "runtime": runtime
        })

    except Exception as e:
        runtime = time.perf_counter() - start

        print(f"[ERROR] Query: {query} -> {e}")

        results.append({
            "query": query,
            "ingredient_match": False,
            "strength_match": False,
            "dosage_match": False,
            "returned_output": False,
            "runtime": runtime,
            "error": str(e)
        })

# Final scoring
final_report = calculate_final_score(results)

# Save results
with open("outputs/evaluation_result.json", "w") as f:
    json.dump(final_report, f, indent=4)

print(json.dumps(final_report, indent=4))