import json
import datetime
import random

default_data = {
    "critical": 0,
    "abnormal": 0,
    "medium": 0,
    "investigated": 0,
    "updated": ""
}

# Load existing data or start fresh
try:
    with open("data.json") as f:
        data = json.load(f)
except FileNotFoundError:
    data = default_data

# Update data randomly but never negative
data["critical"] = max(0, data["critical"] + random.randint(-1, 3))
data["abnormal"] = max(0, data["abnormal"] + random.randint(-2, 5))
data["medium"] = max(0, data["medium"] + random.randint(-1, 2))
data["investigated"] = max(0, data["investigated"] + random.randint(0, 2))

data["updated"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Generate the SVG dashboard with square shape and animations
svg = f"""
<svg width="300" height="300" viewBox="0 0 420 420" xmlns="http://www.w3.org/2000/svg">
  <style>
    .label {{ fill: #cfd8dc; font-size: 16px; font-family: monospace; }}
    .critical {{ fill: #ff1744; font-weight: bold; }}
    .abnormal {{ fill: #ff9100; font-weight: bold; }}
    .medium {{ fill: #ffea00; font-weight: bold; }}
    .investigated {{ fill: #1e90ff; font-weight: bold; }}

    .pulse {{
      animation: pulse 1s ease-in-out infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ fill-opacity: 0.3; }}
      50% {{ fill-opacity: 1; }}
    }}
  </style>

  <rect width="100%" height="100%" rx="15" fill="#0b1c2d"/>

  <!-- Title removed -->

  <text x="30" y="90" class="label critical pulse">Critical: {data["critical"]}</text>
  <text x="30" y="140" class="label abnormal pulse">Abnormal: {data["abnormal"]}</text>
  <text x="30" y="190" class="label medium pulse">Medium: {data["medium"]}</text>
  <text x="30" y="240" class="label investigated pulse">Investigated: {data["investigated"]}</text>

  <text x="20" y="290" class="label" style="font-size: 12px; fill: #78909c;">
    Last Update: {data["updated"]}
  </text>
</svg>
"""

with open("dashboard.svg", "w") as f:
    f.write(svg)

