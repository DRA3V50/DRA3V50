import random
from math import cos, sin, radians
from pathlib import Path

# --- Config ---
WIDTH, HEIGHT = 480, 480
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
RADAR_RADIUS = 200

# Paths
output_live = Path("assets/cyber_radar_live.svg")
output_static = Path("assets/cyber_radar_static.svg")
output_live.parent.mkdir(parents=True, exist_ok=True)

# Realistic cyber blue team nodes
data_points = [
    ("Workstation", 20, 180),
    ("Database Server", 60, 140),
    ("Firewall", 110, 160),
    ("IDS/IPS", 160, 190),
    ("Proxy Server", 210, 150),
    ("Mail Server", 260, 170),
    ("VPN Gateway", 310, 140),
    ("SIEM Node", 350, 190),
]

# --- SVG header ---
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#5cb3ff" flood-opacity="0.8"/>
    </filter>
    <radialGradient id="sweepGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2f6fed" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#2f6fed" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="#0a0f1a"/>

  <!-- Radar rings -->
'''
# Concentric rings
for r in range(40, RADAR_RADIUS + 1, 40):
    svg += f'  <circle cx="{CENTER_X}" cy="{CENTER_Y}" r="{r}" fill="none" stroke="#2f6fed" stroke-width="1" opacity="0.3"/>\n'

# Spokes every 45 degrees (less clutter)
for angle in range(0, 360, 45):
    rad = radians(angle)
    x = CENTER_X + RADAR_RADIUS * cos(rad)
    y = CENTER_Y + RADAR_RADIUS * sin(rad)
    svg += f'  <line x1="{CENTER_X}" y1="{CENTER_Y}" x2="{x}" y2="{y}" stroke="#2f6fed" stroke-width="1" opacity="0.15"/>\n'

# Radar sweep
svg += f'''
  <path d="M{CENTER_X},{CENTER_Y} L{CENTER_X + RADAR_RADIUS},{CENTER_Y} A{RADAR_RADIUS},{RADAR_RADIUS} 0 0,1 {CENTER_X + int(RADAR_RADIUS*0.7)},{CENTER_Y - int(RADAR_RADIUS*0.7)} Z"
        fill="url(#sweepGrad)" filter="url(#glow)">
    <animateTransform attributeName="transform" attributeType="XML" type="rotate"
        from="0 {CENTER_X} {CENTER_Y}" to="360 {CENTER_X} {CENTER_Y}" dur="8s" repeatCount="indefinite"/>
  </path>
'''

# Data points with subtle glow
for label, angle_deg, dist in data_points:
    rad = radians(angle_deg)
    x = CENTER_X + dist * cos(rad)
    y = CENTER_Y + dist * sin(rad)

    svg += f'''
  <circle cx="{x}" cy="{y}" r="8" fill="#5cb3ff" filter="url(#glow)" opacity="0.8">
    <title>{label}</title>
  </circle>
  <text x="{x+10}" y="{y+4}" font-family="Consolas, monospace" font-weight="600"
        font-size="12" fill="#a0c8ff" pointer-events="none">{label}</text>'''

svg += '</svg>'

# --- Write live SVG ---
with open(output_live, "w") as f:
    f.write(svg)

# --- Static SVG for README ---
svg_static = svg.replace('<animateTransform', '<!-- <animateTransform').replace('</animateTransform>', '</animateTransform> -->')
with open(output_static, "w") as f:
    f.write(svg_static)

print("Live and static SVGs generated!")
