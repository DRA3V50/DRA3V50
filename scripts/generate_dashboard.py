import json
import random
from datetime import datetime
from pathlib import Path

# Paths
ASSETS_DIR = Path("assets")
ASSETS_DIR.mkdir(exist_ok=True)
DATA_FILE = ASSETS_DIR / "dashboard_data.json"

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

print("Dashboard JSON updated:", data)
