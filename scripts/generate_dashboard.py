import json
import random
import time
from datetime import datetime
from pathlib import Path

# ----------------------
# CONFIG
# ----------------------
UPDATE_INTERVAL = 5  # seconds

# Paths
ASSETS_DIR = Path("assets")
DATA_FILE = ASSETS_DIR / "dashboard_data.json"

# Ensure assets folder exists
ASSETS_DIR.mkdir(exist_ok=True)

# ----------------------
# LIVE LOOP
# ----------------------
print("Starting live dashboard... Press Ctrl+C to stop.")

try:
    while True:
        # Generate random data
        data = {
            "critical": random.randint(10, 40),
            "abnormal": random.randint(30, 80),
            "medium": random.randint(60, 120),
            "investigated": random.randint(100, 200),
            "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }

        # Save JSON
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

        print("Updated dashboard JSON:", data)

        # Wait before next update
        time.sleep(UPDATE_INTERVAL)

except KeyboardInterrupt:
    print("\nLive dashboard stopped by user.")

