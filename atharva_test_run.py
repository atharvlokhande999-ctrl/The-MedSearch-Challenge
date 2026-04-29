from leaderboard.update_leaderboard import update_leaderboard
import os
import time

def verify_leaderboard_update():
    # 1. Configuration
    username = "Atharva (Developer)"
    sample_score = 75.80  # A test score to see if you climb the ranks
    pr_number = "DEV-01"
    md_path = "leaderboard/leaderboard.md"

    print(f"🚀 Starting Leaderboard Update Test for: {username}")
    
    # 2. Check if file exists before update
    if os.path.exists(md_path):
        print(f"📝 Found existing leaderboard. Size: {os.path.getsize(md_path)} bytes")
    else:
        print("🆕 No leaderboard found. A new one will be created.")

    # 3. Simulate the update process
    print("⏳ Processing update logic...")
    time.sleep(1) # Just for dramatic effect!

    try:
        update_leaderboard(
            username=username,
            pr_number=pr_number,
            score=sample_score,
            status="Testing"
        )
        
        # 4. Verify Success
        if os.path.exists(md_path):
            print(f"✅ SUCCESS: '{md_path}' has been updated!")
            print(f"📈 New Score Recorded: {sample_score}")
            print("\n👉 Open 'leaderboard/leaderboard.md' to see your name in the table!")
        else:
            print("❌ ERROR: The file was not created. Check file permissions.")

    except Exception as e:
        print(f"💥 TEST FAILED: {str(e)}")

if __name__ == "__main__":
    verify_leaderboard_update()