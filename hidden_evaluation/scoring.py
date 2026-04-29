def calculate_final_score(results):
    total = len(results)

    ingredient_hits = sum(r["ingredient_match"] for r in results)
    strength_hits = sum(r["strength_match"] for r in results)
    dosage_hits = sum(r["dosage_match"] for r in results)
    output_hits = sum(r["returned_output"] for r in results)

    avg_runtime = sum(r["runtime"] for r in results) / total

    # Weighted score calculation
    score = (
        (ingredient_hits / total) * 35 +
        (strength_hits / total) * 25 +
        (dosage_hits / total) * 20 +
        (output_hits / total) * 10
    )

    # Speed bonus
    if avg_runtime < 0.5:
        score += 10
    elif avg_runtime < 1:
        score += 5

    score = round(score, 2)

    return {
        "final_score": score,
        "ingredient_accuracy": round((ingredient_hits / total) * 100, 2),
        "strength_accuracy": round((strength_hits / total) * 100, 2),
        "dosage_accuracy": round((dosage_hits / total) * 100, 2),
        "output_return_rate": round((output_hits / total) * 100, 2),
        "avg_runtime": round(avg_runtime, 4)
    }