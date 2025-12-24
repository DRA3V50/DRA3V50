import subprocess
import json
from datetime import datetime, timedelta

LOOKBACK_HOURS = 24
cutoff = datetime.utcnow() - timedelta(hours=LOOKBACK_HOURS)

with open("radar-config.json") as f:
    config = json.load(f)

results = []

for label, meta in config.items():
    repo = meta["repo"]

    try:
        output = subprocess.check_output([
            "git", "log",
            f"--since={cutoff.isoformat()}",
            "--oneline"
        ], cwd=f"../{repo}", stderr=subprocess.DEVNULL)

        commits = len(output.decode().strip().splitlines())
    except Exception:
        commits = 0

    results.append(commits)

# normalize to 0–1
max_commits = max(results) if max(results) > 0 else 1
normalized = [round(c / max_commits, 2) for c in results]

with open("radar-values.json", "w") as f:
    json.dump(normalized, f)

