import json
import random
import time
from datetime import datetime
from pathlib import Path

# Paths
ASSETS_DIR = Path("assets")
DATA_FILE = ASSETS_DIR / "dashboard_data.json"
SVG_FILE = ASSETS_DIR / "live_dashboard.svg"

# Ensure assets folder exists
ASSETS_DIR.mkdir(exist_ok=True)

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

def build_svg(data):
    # SVG with simple color pulse animation for metrics
    svg = f"""
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

  <text x="20" y="60" class="metric critical">
    Critical Alerts: {data.get("critical",0)}
    <animate attributeName="fill" values="#ef4444;#ff6666;#ef4444" dur="0.5s" begin="0s" repeatCount="1" />
  </text>
  <text x="20" y="90" class="metric high">
    Abnormal Alerts: {data.get("abnormal",0)}
    <animate attributeName="fill" values="#f97316;#ffae5c;#f97316" dur="0.5s" begin="0s" repeatCount="1" />
  </text>
  <text x="20" y="120" class="metric medium">
    Medium Severity: {data.get("medium",0)}
    <animate attributeName="fill" values="#facc15;#fff48f;#facc15" dur="0.5s" begin="0s" repeatCount="1" />
  </text>

  <text x="20" y="150" class="metric ok">
    Investigated: {data.get("investigated",0)}
    <animate attributeName="fill" values="#22c55e;#7fe77f;#22c55e" dur="0.5s" begin="0s" repeatCount="1" />
  </text>
  <text x="20" y="165" class="small">Updated: {data.get("updated","")}</text>
</svg>
"""
    with open(SVG_FILE, "w") as f:
        f.write(svg)

print("Live dashboard running... press Ctrl+C to stop")

# Loop to update every 10 seconds
try:
    while True:
        data = generate_data()
        save_json(data)
        build_svg(data)
        time.sleep(10)  # update interval in seconds
except KeyboardInterrupt:
    print("\nStopped live dashboard.")
