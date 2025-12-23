import json
from datetime import datetime
import os

# --- Paths ---
DATA_FILE = "scripts/data.json"
OUTPUT_SVG = "assets/intel_dashboard.svg"

# Ensure assets folder exists
os.makedirs(os.path.dirname(OUTPUT_SVG), exist_ok=True)

# --- Lane definitions ---
lanes = [
    {"name": "SOC", "color": "#00ffff"},
    {"name": "IR", "color": "#ffa500"},
    {"name": "SIEM", "color": "#1e90ff"},
    {"name": "SOAR", "color": "#9932cc"},
    {"name": "EDR", "color": "#32cd32"},
    {"name": "Data Automation", "color": "#ff69b4"},
    {"name": "Data Analysis & Intelligence", "color": "#ffff00"},
]

SVG_WIDTH = 1000
SVG_HEIGHT = 600
LANE_WIDTH = SVG_WIDTH // len(lanes)
BORDER = 50
BLIP_SPACING = 50

# --- Load JSON data ---
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    # default counts if JSON missing
    data = {lane["name"]: 3 for lane in lanes}

# --- Start SVG ---
svg_elements = []
svg_elements.append(f'<svg width="{SVG_WIDTH}" height="{SVG_HEIGHT}" xmlns="http://www.w3.org/2000/svg">')
svg_elements.append(f'<rect width="100%" height="100%" fill="#0a0a23"/>')  # dark background

# --- Draw lanes and blips ---
for idx, lane in enumerate(lanes):
    x = idx * LANE_WIDTH
    # Lane background
    svg_elements.append(f'<rect x="{x}" y="0" width="{LANE_WIDTH}" height="{SVG_HEIGHT}" fill="#101040" opacity="0.8"/>')
    # Lane icon as small circle
    svg_elements.append(f'<circle cx="{x + 20}" cy="{BORDER/2}" r="8" fill="{lane["color"]}" />')
    # Lane title
    svg_elements.append(f'<text x="{x + 40}" y="{BORDER/2 + 5}" font-size="14" fill="{lane["color"]}">{lane["name"]}</text>')

    # Blips for activity
    count = data.get(lane["name"], 0)
    for i in range(count):
        blip_x = x + LANE_WIDTH/2
        blip_y = BORDER + 30 + i * BLIP_SPACING
        svg_elements.append(f'<circle cx="{blip_x}" cy="{blip_y}" r="15" fill="{lane["color"]}">')
        svg_elements.append(f'<title>{lane["name"]} activity {i+1}</title>')  # hover title
        svg_elements.append('</circle>')

# --- Footer timestamp ---
now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
svg_elements.append(f'<text x="{SVG_WIDTH/2}" y="{SVG_HEIGHT - 20}" text-anchor="middle" font-size="14" fill="#aaa">Last update: {now}</text>')

svg_elements.append('</svg>')

# --- Write SVG ---
with open(OUTPUT_SVG, "w") as f:
    f.write("\n".join(svg_elements))

print(f"Generated {OUTPUT_SVG}")
