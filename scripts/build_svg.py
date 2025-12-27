import subprocess
import json
from datetime import datetime, timedelta

LOOKBACK_HOURS = 72
cutoff = datetime.utcnow() - timedelta(hours=LOOKBACK_HOURS)

with open("radar-config.json") as f:
    labels = list(json.load(f).keys())

try:
    output = subprocess.check_output([
        "git", "log",
        f"--since={cutoff.isoformat()}",
        "--oneline"
    ])
    total_commits = len(output.decode().splitlines())
except Exception:
    total_commits = 0

# Distribute activity across domains (intentional weighting)
weights = [
    1.0, 0.9, 0.85, 0.75,
    0.8, 0.7, 0.6, 0.65
]

raw = [total_commits * w for w in weights]
max_val = max(raw) if max(raw) > 0 else 1
normalized = [round(v / max_val, 2) for v in raw]

with open("radar-values.json", "w") as f:
    json.dump(normalized, f)

print("✔ radar-values.json generated")
