import os
import subprocess
import math
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------
DAYS_LOOKBACK = 30
OUTPUT_FILE = "assets/blue-team-radar.svg"

AXES = {
    "SOC Operations": ["SOC", "IR", ".md"],
    "Incident Response": ["incident", "response", "playbook"],
    "Threat Detection": ["detection", "siem", "alert"],
    "Automation": [".py", ".ps1", ".sql"],
    "Data & Analytics": ["sql", "powerbi", "report"],
    "Cloud Security": ["azure", "aws", "cloud"]
}

# ----------------------------------------

def get_commits():
    since = (datetime.utcnow() - timedelta(days=DAYS_LOOKBACK)).isoformat()
    cmd = [
        "git", "log",
        f"--since={since}",
        "--name-only",
        "--pretty=format:"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.lower().splitlines()

def score_axes(files):
    scores = {k: 0 for k in AXES}
    for f in files:
        for axis, keywords in AXES.items():
            if any(k in f for k in keywords):
                scores[axis] += 1
    max_score = max(scores.values()) or 1
    return {k: int((v / max_score) * 100) for k, v in scores.items()}

def generate_svg(scores):
    labels = list(scores.keys())
    values = list(scores.values())
    count = len(labels)

    cx, cy, r = 200, 200, 140
    points = []

    for i, v in enumerate(values):
        angle = (2 * math.pi / count) * i - math.pi / 2
        radius = r * (v / 100)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append(f"{x},{y}")

    svg = f"""<svg width="400" height="400" viewBox="0 0 400 400"
xmlns="http://www.w3.org/2000/svg">
<style>
polygon {{
  fill: rgba(0, 180, 255, 0.25);
  stroke: #00b4ff;
  stroke-width: 2;
  animation: pulse 6s infinite alternate;
}}
text {{
  fill: #cfefff;
  font-size: 12px;
  text-anchor: middle;
}}
@keyframes pulse {{
  from {{ fill-opacity: 0.2; }}
  to {{ fill-opacity: 0.4; }}
}}
</style>

<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1e2a38"/>
<polygon points="{' '.join(points)}"/>
"""

    for i, label in enumerate(labels):
        angle = (2 * math.pi / count) * i - math.pi / 2
        x = cx + (r + 20) * math.cos(angle)
        y = cy + (r + 20) * math.sin(angle)
        svg += f'<text x="{x}" y="{y}">{label}</text>\n'

    svg += "</svg>"
    return svg

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    commits = get_commits()
    scores = score_axes(commits)
    svg = generate_svg(scores)

    with open(OUTPUT_FILE, "w") as f:
        f.write(svg)
