import json
import random
import time
from datetime import datetime
from pathlib import Path
import os

# ----------------------
# CONFIG
# ----------------------
UPDATE_INTERVAL = 5  # seconds

# Detect if running in CI/GitHub Actions
IN_CI = os.getenv("GITHUB_ACTIONS") == "true"

# Paths
ASSETS_DIR = Path("assets")
DATA_FILE = ASSETS_DIR / "dashboard_data.json"

# Ensure assets folder exists
ASSETS_DIR.mkdir(exist_ok=True)

# ----------------------
# FUNCTIONS
# ----------------------
def generate_data():
    return {
        "critical": random.randint(10, 40),
        "abnormal": random.randint(30, 80),
        "medium": random.randint(60, 120),
        "investigated": random.randint(100, 200),
        "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

def save_json(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ----------------------
# MAIN
# ----------------------
def main():
    if IN_CI:
        # Single run for GitHub Actions
        data = generate_data()
        save_json(data)
        print("Dashboard updated successfully (CI mode).")
    else:
        # Live local mode
        print("Starting live dashboard... Press Ctrl+C to stop.")
        try:
            while True:
                data = generate_data()
                save_json(data)
                print("Updated dashboard JSON:", data)
                time.sleep(UPDATE_INTERVAL)
        except KeyboardInterrupt:
            print("\nLive dashboard stopped by user.")

if __name__ == "__main__":
    main()

