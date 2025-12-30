import json
import random
from datetime import datetime
from pathlib import Path

# Paths
ASSETS_DIR = Path("assets")
DATA_FILE = ASSETS_DIR / "dashboard_data.json"
SVG_FILE = ASSETS_DIR / "live_dashboard.svg"

# Ensure assets folder exists
ASSETS_DIR.mkdir(exist_ok=True)

# Generate live-ish data
data = {
    "critical": random.randint(10, 40),
    "abnormal": random.randint(30, 80),  # Using 'abnormal' instead of 'high severity'
    "medium": random.randint(60, 120),
    "investigated": random.randint(100, 200),
    "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
}

# Save JSON
with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

# Build SVG dashboard
svg = f"""
<svg width="300" height="180" xmlns="http://www.w3.org/2000/svg">
  <style>
    text {{ font-family: Arial, sans-serif; fill: #e5e7eb; }}
    .title {{ font-size: 22px; font-weight: bold; }}
    .metric {{ font-size: 18px; }}
    .critical {{ fill: #ef4444; }}
    .high {{ fill: #f97316; }}
    .medium {{ fill: #facc15; }}
    .ok {{ fill: #22c55e; }}
    .small {{ font-size: 12px; fill: #94a3b8; }}
  </style>

  <rect width="100%" height="100%" rx="12" fill="#0f172a"/>

  <text x="20" y="32" class="title">Threat Intelligence Dashboard</text>

  <text x="20" y="70" class="metric critical">Critical Alerts: {data.get("critical",0)}</text>
  <text x="20" y="100" class="metric high">Abnormal Alerts: {data.get("abnormal",0)}</text>
  <text x="20" y="130" class="metric medium">Medium Severity: {data.get("medium",0)}</text>

  <text x="20" y="160" class="metric ok">Investigated: {data.get("investigated",0)}</text>
  <text x="20" y="175" class="small">Updated: {data.get("updated","")}</text>
</svg>
"""

# Save SVG
with open(SVG_FILE, "w") as f:
    f.write(svg)

print("Dashboard updated successfully")
