import json

# Load evaluation results
with open("outputs/evaluation_result.json", "r") as f:
    data = json.load(f)

# Create markdown content
readme_content = f"""
# 🏆 Medicine Recommendation System

## 📊 Leaderboard

| Metric | Score |
|--------|------|
| **Final Score** | **{data['final_score']:.2f}** |
| Ingredient Accuracy | {data['ingredient_accuracy']:.2f}% |
| Strength Accuracy | {data['strength_accuracy']:.2f}% |
| Dosage Accuracy | {data['dosage_accuracy']:.2f}% |
| Output Return Rate | {data['output_return_rate']:.2f}% |
| Avg Runtime | {data['avg_runtime']:.4f} sec |

---

## 📌 Project Overview
This system recommends alternative medicines based on brand name using a similarity-based ranking approach.

---

## 🚀 Key Features
- Fuzzy matching for brand names
- Weighted scoring system
- Fast evaluation pipeline
- Robust handling of missing data

---

## 📈 Performance Summary
The model performs best in dosage prediction and has room for improvement in ingredient and strength matching.

"""

# Write to README
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("README updated successfully!")