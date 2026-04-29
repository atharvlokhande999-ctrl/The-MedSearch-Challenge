import json
import csv
import os
from datetime import datetime

def update_leaderboard(username, pr_number, score, status="Accepted"):
    json_path = "leaderboard/leaderboard.json"
    md_path = "leaderboard/leaderboard.md"
    log_path = "leaderboard/submissions_log.csv"
    
    # 1. Load existing data (Using utf-8)
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            leaderboard = json.load(f)
    else:
        leaderboard = []

    # 2. Add new entry
    leaderboard.append({
        "username": username,
        "score": round(float(score), 2),
        "pr_number": pr_number,
        "date": datetime.now().strftime("%Y-%m-%d")
    })

    # 3. Sort by score (High to Low)
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)

    # 4. Save JSON Database (Using utf-8)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, indent=4)

    # 5. Automatically Write/Update leaderboard.md (Using utf-8)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 🏆 Competition Leaderboard\n\n")
        f.write("Welcome to the MedSearch optimization challenge. Rankings update automatically on merge.\n\n")
        f.write("| Rank | Contributor | Score | PR # | Date |\n")
        f.write("|:---:|:---|:---:|:---:|:---:|\n")
        
        for idx, entry in enumerate(leaderboard, start=1):
            f.write(f"| {idx} | **{entry['username']}** | {entry['score']} | #{entry['pr_number']} | {entry['date']} |\n")

    # 6. Update CSV Log (Using utf-8)
    file_exists = os.path.isfile(log_path)
    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Username", "PR_Number", "Score", "Status", "Date"])
        writer.writerow([username, pr_number, score, status, datetime.now().strftime("%Y-%m-%d")])

    print(f"✅ Success: Leaderboard and Markdown table updated for {username}!")