from baseline_code.recommender import recommend_alternatives
from leaderboard.update_leaderboard import update_leaderboard
import time

# 1. Run a test search
print("Testing Allegra...")
start_time = time.time()
results = recommend_alternatives("Allegra 120mg Tablet")
end_time = time.time()

# 2. Display results in terminal
print(results)

# 3. Simulate a score for this local test
# In a real run, the evaluator calculates this. 
# Here, we'll assume a successful return equals a test score.
if not results.empty:
    test_score = 46.15  # You can manually update this number based on evaluator.py
    runtime = end_time - start_time
    
    print(f"\nMatch found in {runtime:.4f}s. Updating local leaderboard...")
    
    # 4. TRIGGER THE LEADERBOARD UPDATE
    # This will create/update leaderboard/leaderboard.md immediately
    update_leaderboard(
        username="Local-Test-User", 
        pr_number="TEST", 
        score=test_score
    )
    
    print("Done! Check leaderboard/leaderboard.md to see the change.")
else:
    print("\nNo results found. Leaderboard not updated.")