# Contributing to MedSearch Challenge

Thank you for participating in the MedSearch GitHub Optimization Challenge.

Please follow these instructions carefully.

---

## Step 1 — Fork the Repository

Click the Fork button on top right of this repository.

---

## Step 2 — Clone Your Fork

git clone <your-fork-url>

---

## Step 3 — Modify Only This File

baseline_code/recommender.py

Do not rename function.

---

## Step 4 — Install Dependencies

pip install -r baseline_code/requirements.txt

---

## Step 5 — Test Your Code Locally

Make sure your recommender function runs without errors.

---

## Step 6 — Push Changes To Your Fork

git add .
git commit -m "Improved medicine recommender"
git push origin main

---

## Step 7 — Create Pull Request

Open Pull Request to this main repository.

Your PR will be automatically evaluated.

---

## Evaluation Criteria

- Ingredient correctness
- Strength correctness
- Dosage form correctness
- Runtime speed
- Robustness to medicine name variations

---

## Important Restrictions

Do not modify:

- hidden_evaluation/
- leaderboard/
- .github/workflows/

Only `baseline_code/recommender.py` is allowed.