import json
import os

# Ensure data.json exists
if not os.path.exists("data.json"):
    data = {
        "critical": 0,
        "abnormal": 0,
        "medium": 0,
        "investigated": 0,
        "updated": "N/A"
    }
else:
    with open("data.json") as f:
        data = json.load(f)

svg = f"""
<svg width="420" height="220" viewBox="0 0 420 220"
     xmlns="http://www.w3.org/2000/svg">

  <style>
    .title {{ fill: #00e5ff; font-size: 18px; font-family: monospace; }}
    .label {{ fill: #cfd8dc; font-size: 14px; font-family: monospace; }}
    .critical {{ fill: #ff1744; }}
    .abnormal {{ fill: #ff9100; }}
    .medium {{ fill: #ffea00; }}
    .investigated {{ fill: #00e676; }}
    .footer {{ fill: #78909c; font-size: 11px; }}

    .pulse {{
      animation: pulse 1.8s infinite;
    }}

    @keyframes pulse {{
      0% {{ opacity: 0.6; }}
      50% {{ opacity: 1; }}
      100% {{ opacity: 0.6; }}
    }}
  </style>

  <rect width="100%" height="100%" rx="15" fill="#0b1c2d"/>

  <text x="20" y="30" class="title">🛡 SOC Live Alert Dashboard</text>

  <text x="30" y="70" class="label critical pulse">
    Critical: {data["critical"]}
  </text>

  <text x="30" y="100" class="label abnormal">
    Abnormal: {data["abnormal"]}
  </text>

  <text x="30" y="130" class="label medium">
    Medium: {data["medium"]}
  </text>

  <text x="30" y="160" class="label investigated">
    Investigated: {data["investigated"]}
  </text>

  <text x="20" y="200" class="footer">
    Last Update: {data["updated"]}
  </text>
</svg>
"""

with open("dashboard.svg", "w") as f:
    f.write(svg)
