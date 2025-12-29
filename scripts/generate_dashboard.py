import json
from datetime import datetime
import random

with open("dashboard/data.json", "r") as f:
    data = json.load(f)

# Simulate live SOC changes
data["critical"] = random.randint(20, 30)
data["high"] = random.randint(45, 70)
data["medium"] = random.randint(70, 110)
data["investigated"] += random.randint(1, 5)
data["last_updated"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

with open("dashboard/data.json", "w") as f:
    json.dump(data, f, indent=2)

svg = f"""
<svg width="800" height="260" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{ font: bold 24px sans-serif; fill: #e5e7eb; }}
    .label {{ font: 14px sans-serif; fill: #9ca3af; }}
    .critical {{ fill: #ef4444; }}
    .high {{ fill: #f97316; }}
    .medium {{ fill: #eab308; }}
    .ok {{ fill: #22c55e; }}
  </style>

  <rect width="100%" height="100%" rx="15" fill="#0f172a"/>

  <text x="30" y="40" class="title">Live Security Anomaly Telemetry</text>

  <text x="30" y="90" class="label">Critical Alerts</text>
  <text x="30" y="120" class="critical">{data['critical']}</text>

  <text x="200" y="90" class="label">High Severity</text>
  <text x="200" y="120" class="high">{data['high']}</text>

  <text x="370" y="90" class="label">Medium Severity</text>
  <text x="370" y="120" class="medium">{data['medium']}</text>

  <text x="570" y="90" class="label">Investigated</text>
  <text x="570" y="120" class="ok">{data['investigated']}</text>

  <text x="30" y="210" class="label">Last Update: {data['last_updated']}</text>
</svg>
"""

with open("dashboard/dashboard.svg", "w") as f:
    f.write(svg)

