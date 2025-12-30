import json
import random
from datetime import datetime
from pathlib import Path

ASSETS_DIR = Path("assets")
SVG_FILE = ASSETS_DIR / "live_dashboard.svg"

ASSETS_DIR.mkdir(exist_ok=True)

# Generate random data
data = {
    "critical": random.randint(10, 40),
    "abnormal": random.randint(30, 80),
    "medium": random.randint(60, 120),
    "investigated": random.randint(100, 200),
    "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
}

# Build SVG
svg_content = f"""
<svg width="300" height="180" xmlns="http://www.w3.org/2000/svg">
  <style>
    text {{ font-family: Arial, sans-serif; fill: #e5e7eb; }}
    .title {{ font-size: 16px; font-weight: bold; }}
    .metric {{ font-size: 18px; }}
    .critical {{ fill: #ef4444; }}
    .high {{ fill: #f97316; }}
    .medium {{ fill: #facc15; }}
    .ok {{ fill: #22c55e; }}
    .small {{ font-size: 12px; fill: #94a3b8; }}
  </style>
  <rect width="100%" height="100%" rx="12" fill="#0f172a"/>
  <text x="20" y="28" class="title">Threat Intelligence Dashboard</text>
  <text x="20" y="60" class="metric critical">Critical Alerts: {data["critical"]}</text>
  <text x="20" y="90" class="metric high">Abnormal Alerts: {data["abnormal"]}</text>
  <text x="20" y="120" class="metric medium">Medium Severity: {data["medium"]}</text>
  <text x="20" y="150" class="metric ok">Investigated: {data["investigated"]}</text>
  <text x="20" y="165" class="small">Updated: {data["updated"]}</text>
</svg>
"""

with open(SVG_FILE, "w") as f:
    f.write(svg_content)

print("SVG dashboard updated")
