import json
from datetime import datetime

# Path to JSON data (replace with GitHub API data later if you want)
DATA_FILE = "scripts/data.json"
OUTPUT_SVG = "intel_dashboard.svg"

# Lane definitions
lanes = [
    {"name": "SOC", "icon": "🛡️", "color": "#00ffff"},
    {"name": "IR", "icon": "🕵️‍♂️", "color": "#ffa500"},
    {"name": "SIEM", "icon": "📊", "color": "#1e90ff"},
    {"name": "SOAR", "icon": "⚙️", "color": "#9932cc"},
    {"name": "EDR", "icon": "💻", "color": "#32cd32"},
    {"name": "Data Automation", "icon": "🤖", "color": "#ff69b4"},
    {"name": "Data Analysis & Intelligence", "icon": "📈", "color": "#ffff00"},
]

SVG_WIDTH = 1000
SVG_HEIGHT = 600
LANE_WIDTH = SVG_WIDTH // len(lanes)
BORDER = 50

# Load JSON data
try:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    # Default data if JSON not present
    data = {lane["name"]: 3 for lane in lanes}

# Start SVG
svg_elements = []
svg_elements.append(f'<svg width="{SVG_WIDTH}" height="{SVG_HEIGHT}" xmlns="http://www.w3.org/2000/svg">')
svg_elements.append(f'<rect width="100%" height="100%" fill="#0a0a23"/>')  # background

# Draw lanes
for idx, lane in enumerate(lanes):
    x = idx * LANE_WIDTH
    # Lane background
    svg_elements.append(f'<rect x="{x}" y="0" width="{LANE_WIDTH}" height="{SVG_HEIGHT}" fill="#101040" opacity="0.8"/>')
    # Lane title
    svg_elements.append(f'<text x="{x + LANE_WIDTH/2}" y="{BORDER/2}" text-anchor="middle" font-size="18" fill="{lane["color"]}">{lane["icon"]} {lane["name"]}</text>')
    
    # Draw blips/cards
    count = data.get(lane["name"], 0)
    for i in range(count):
        blip_x = x + LANE_WIDTH/2
        blip_y = BORDER + 50 + i*50
        # pulsing circle
        svg_elements.append(f'''
        <circle cx="{blip_x}" cy="{blip_y}" r="15" fill="{lane["color"]}">
            <animate attributeName="r" values="10;20;10" dur="2s" repeatCount="indefinite"/>
        </circle>
        ''')

# Footer timestamp
now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
svg_elements.append(f'<text x="{SVG_WIDTH/2}" y="{SVG_HEIGHT - 20}" text-anchor="middle" font-size="14" fill="#aaa">Last update: {now}</text>')

svg_elements.append('</svg>')

# Write SVG
with open(OUTPUT_SVG, "w") as f:
    f.write("\n".join(svg_elements))

print(f"Generated {OUTPUT_SVG}")

