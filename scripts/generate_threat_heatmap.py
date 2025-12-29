import json
import random
from datetime import datetime

# Load coverage / host data
try:
    with open("radar-config.json") as f:
        hosts = json.load(f)
except FileNotFoundError:
    # sample data if config missing
    hosts = [
        {"name": "HostA", "x": 100, "y": 80, "tactic": "Initial Access"},
        {"name": "Server42", "x": 300, "y": 150, "tactic": "Execution"},
        {"name": "DBServer", "x": 500, "y": 220, "tactic": "Persistence"},
        {"name": "Firewall", "x": 400, "y": 300, "tactic": "Defense Evasion"},
    ]

# Generate dynamic activity levels
for host in hosts:
    host["activity"] = random.randint(0, 100)  # intensity 0-100

# SVG header
svg_header = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400">
  <rect width="600" height="400" fill="#0a0f1a"/>
  <defs>
    <radialGradient id="pulseGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff4e4e" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#ff4e4e" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <text x="10" y="20" fill="#a0c8ff" font-family="Consolas, monospace" font-size="14">
    Last Updated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC
  </text>
'''

# Generate hosts as animated circles
host_svgs = ""
for h in hosts:
    radius = 6 + h["activity"] / 20  # pulsing radius based on activity
    pulse_duration = 2 + h["activity"] / 50
    color = "#4effff" if h["activity"] < 50 else "#ff4e4e"
    host_svgs += f'''
  <circle cx="{h['x']}" cy="{h['y']}" r="{radius}" fill="{color}">
    <animate attributeName="r" values="{radius};{radius+4};{radius}" dur="{pulse_duration}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.5;1;0.5" dur="{pulse_duration}s" repeatCount="indefinite"/>
    <title>{h['name']} ({h['tactic']})</title>
  </circle>
  <text x="{h['x']+10}" y="{h['y']+5}" font-family="Consolas, monospace" font-size="12" fill="#a0c8ff">{h['name']}</text>
'''

# Close SVG
svg_footer = "</svg>"

# Write to assets
with open("assets/threat_heatmap_live.svg", "w") as f:
    f.write(svg_header + host_svgs + svg_footer)

