import json
import datetime
import random

# -----------------------------
# Load or initialize data
# -----------------------------
default_data = {
    "critical": 0,
    "abnormal": 0,
    "medium": 0,
    "investigated": 0,
    "updated": ""
}

try:
    with open("data.json") as f:
        data = json.load(f)
except FileNotFoundError:
    data = default_data

# Update numbers randomly
data["critical"] = max(0, data["critical"] + random.randint(-1, 3))
data["abnormal"] = max(0, data["abnormal"] + random.randint(-2, 5))
data["medium"] = max(0, data["medium"] + random.randint(-1, 2))
data["investigated"] = max(0, data["investigated"] + random.randint(0, 2))

data["updated"] = datetime.datetime.estnow().strftime("%Y-%m-%d %H:%M:%S EST")

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# -----------------------------
# Generate SVG
# -----------------------------
svg = f"""
<svg width="420" height="420" viewBox="0 0 420 420" xmlns="http://www.w3.org/2000/svg">
  <style>
    .label {{ fill: #cfd8dc; font-size: 20px; font-family: monospace; }}
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

    /* Flickering magnifying glass */
    .scanner {{
      animation: scannerFlicker 1.2s infinite alternate;
    }}
    @keyframes scannerFlicker {{
      0% {{ fill: #00bfff; opacity: 0.6; }}
      25% {{ fill: #1e90ff; opacity: 1; }}
      50% {{ fill: #87cefa; opacity: 0.8; }}
      75% {{ fill: #00bfff; opacity: 1; }}
      100% {{ fill: #1e90ff; opacity: 0.7; }}
    }}
  </style>

  <!-- Background -->
  <rect width="100%" height="100%" rx="15" fill="#0b1c2d"/>

  <!-- Numbers -->
  <text x="40" y="110" class="label critical pulse">Critical: {data["critical"]}</text>
  <text x="40" y="170" class="label abnormal pulse">Abnormal: {data["abnormal"]}</text>
  <text x="40" y="230" class="label medium pulse">Medium: {data["medium"]}</text>
  <text x="40" y="290" class="label investigated pulse">Investigated: {data["investigated"]}</text>

  <!-- Footer -->
  <text x="40" y="360" class="label" style="font-size: 14px; fill: #78909c;">
    Last Update: {data["updated"]}
  </text>

  <!-- Magnifying glass emoji top-right -->
  <text x="360" y="50" font-size="32" class="scanner">🔍</text>
</svg>
"""

with open("dashboard.svg", "w") as f:
    f.write(svg)

