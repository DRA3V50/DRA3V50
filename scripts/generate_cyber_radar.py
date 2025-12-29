from pathlib import Path
from math import sin, cos, radians

WIDTH, HEIGHT = 480, 480
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
RADAR_RADIUS = 200

output = Path("assets/cyber_radar_static.svg")
output.parent.mkdir(parents=True, exist_ok=True)

data_points = [
    ("HostA", 15, 180),
    ("Server42", 75, 130),
    ("Workstation12", 130, 160),
    ("Router1", 200, 190),
    ("DBServer", 265, 150),
]

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <rect width="{WIDTH}" height="{HEIGHT}" fill="#0a0f1a"/>
'''

# Draw radar rings
for r in range(40, RADAR_RADIUS + 1, 40):
    svg += f'<circle cx="{CENTER_X}" cy="{CENTER_Y}" r="{r}" fill="none" stroke="#2f6fed" stroke-width="1" opacity="0.3"/>\n'

# Draw spokes every 45 degrees
for angle in range(0, 360, 45):
    rad = radians(angle)
    x = CENTER_X + RADAR_RADIUS * cos(rad)
    y = CENTER_Y + RADAR_RADIUS * sin(rad)
    svg += f'<line x1="{CENTER_X}" y1="{CENTER_Y}" x2="{x}" y2="{y}" stroke="#2f6fed" stroke-width="1" opacity="0.2"/>\n'

# Draw data points
for label, angle_deg, dist in data_points:
    rad = radians(angle_deg)
    x = CENTER_X + dist * cos(rad)
    y = CENTER_Y + dist * sin(rad)
    svg += f'<circle cx="{x}" cy="{y}" r="6" fill="#5cb3ff"/>\n'
    svg += f'<text x="{x + 8}" y="{y + 4}" font-family="Consolas, monospace" font-size="12" fill="#a0c8ff">{label}</text>\n'

svg += '</svg>'

with open(output, "w") as f:
    f.write(svg)

print(f"Static Cyber Radar SVG saved to {output}")

