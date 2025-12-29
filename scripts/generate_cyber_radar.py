import random
from math import cos, sin, radians
from pathlib import Path

# --- CONFIG ---
WIDTH, HEIGHT = 480, 480
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
RADAR_RADIUS = 200

output = Path("assets/cyber_radar_static.svg")
output.parent.mkdir(parents=True, exist_ok=True)

# Example data points: (label, angle in degrees, distance from center)
data_points = [
    ("HostA", 15, 180),
    ("Server42", 75, 130),
    ("Workstation12", 130, 160),
    ("Router1", 200, 190),
    ("DBServer", 265, 150),
    ("Firewall", 320, 170),
    ("HostB", 355, 140),
    ("SensorX", 50, 190),
    ("Node9", 105, 125),
    ("Proxy", 185, 130),
]

# --- START SVG ---
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <!-- Background -->
  <rect width="{WIDTH}" height="{HEIGHT}" fill="#0a0f1a"/>
  
  <!-- Radar rings -->
'''

# Draw concentric rings
for r in range(40, RADAR_RADIUS + 1, 40):
    svg += f'  <circle cx="{CENTER_X}" cy="{CENTER_Y}" r="{r}" fill="none" stroke="#2f6fed" stroke-width="1" opacity="0.3"/>\n'

# Draw spokes every 30 degrees
for angle in range(0, 360, 30):
    rad = radians(angle)
    x = CENTER_X + RADAR_RADIUS * cos(rad)
    y = CENTER_Y + RADAR_RADIUS * sin(rad)
    svg += f'  <line x1="{CENTER_X}" y1="{CENTER_Y}" x2="{x}" y2="{y}" stroke="#2f6fed" stroke-width="1" opacity="0.15"/>\n'

# Draw data points with labels
for label, angle_deg, dist in data_points:
    rad = radians(angle_deg)
    x = CENTER_X + dist * cos(rad)
    y = CENTER_Y + dist * sin(rad)

    # Main dot
    svg += f'  <circle cx="{x}" cy="{y}" r="6" fill="#5cb3ff" opacity="0.9"/>\n'

    # Label
    svg += f'  <text x="{x + 12}" y="{y + 5}" font-family="Consolas, monospace" font-weight="600" font-size="14" fill="#a0c8ff">{label}</text>\n'

# Optional: central title
svg += f'''  <text x="{CENTER_X}" y="30" font-family="Consolas, monospace" font-weight="700" font-size="18" fill="#9ec7ff" text-anchor="middle">Cyber Radar</text>
</svg>'''

# Write to file
with open(output, "w") as f:
    f.write(svg)

print(f"Static Cyber Radar SVG saved to {output}")

