import random
from math import cos, sin, radians
from pathlib import Path

WIDTH, HEIGHT = 480, 480
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
RADAR_RADIUS = 200

output = Path("assets/cyber_radar_advanced.svg")
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

# SVG header and background
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <!-- Glow filter -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#5cb3ff" flood-opacity="0.8"/>
    </filter>
    <!-- Blur behind dots -->
    <filter id="blurGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="blur"/>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Sweep gradient -->
    <radialGradient id="sweepGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2f6fed" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#2f6fed" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Background -->
  <rect width="{WIDTH}" height="{HEIGHT}" fill="#0a0f1a"/>

  <!-- Radar rings -->
'''

# Draw concentric rings
for r in range(40, RADAR_RADIUS + 1, 40):
    svg += f'  <circle cx="{CENTER_X}" cy="{CENTER_Y}" r="{r}" fill="none" stroke="#2f6fed" stroke-width="1" opacity="0.3"/>\n'

# Draw spokes every 30 degrees for finer grid
for angle in range(0, 360, 30):
    rad = radians(angle)
    x = CENTER_X + RADAR_RADIUS * cos(rad)
    y = CENTER_Y + RADAR_RADIUS * sin(rad)
    svg += f'  <line x1="{CENTER_X}" y1="{CENTER_Y}" x2="{x}" y2="{y}" stroke="#2f6fed" stroke-width="1" opacity="0.15"/>\n'

# Sweep radar beam (rotating semi-transparent circle segment with glow)
svg += f'''
  <path d="M{CENTER_X},{CENTER_Y} L{CENTER_X + RADAR_RADIUS}, {CENTER_Y} A{RADAR_RADIUS},{RADAR_RADIUS} 0 0,1 {CENTER_X + int(RADAR_RADIUS*0.7)}, {CENTER_Y - int(RADAR_RADIUS*0.7)} Z"
        fill="url(#sweepGrad)" filter="url(#glow)">
    <animateTransform attributeName="transform" attributeType="XML" type="rotate" from="0 {CENTER_X} {CENTER_Y}" to="360 {CENTER_X} {CENTER_Y}" dur="8s" repeatCount="indefinite" />
  </path>
'''

# Draw data points with pulsing + glowing effects and labels
for label, angle_deg, dist in data_points:
    rad = radians(angle_deg)
    x = CENTER_X + dist * cos(rad)
    y = CENTER_Y + dist * sin(rad)
    dur = round(random.uniform(2.5, 4.5), 2)
    begin = round(random.uniform(0, 4), 2)

    # Blurred glow circle behind main dot for tech effect
    svg += f'''
  <circle cx="{x}" cy="{y}" r="10" fill="#5cb3ff" opacity="0.15" filter="url(#blurGlow)">
    <animate attributeName="opacity" values="0.15;0.3;0.15" dur="{dur}s" repeatCount="indefinite" begin="{begin}s"/>
  </circle>'''

    # Main pulsing dot
    svg += f'''
  <circle cx="{x}" cy="{y}" r="6" fill="#5cb3ff" filter="url(#glow)" opacity="0.8">
    <animate attributeName="r" values="6;10;6" dur="{dur}s" repeatCount="indefinite" begin="{begin}s"/>
    <animate attributeName="opacity" values="0.8;1;0.8" dur="{dur}s" repeatCount="indefinite" begin="{begin}s"/>
    <title>{label}</title>
  </circle>'''

    # Label with subtle drop shadow
    svg += f'''
  <text x="{x + 12}" y="{y + 5}" font-family="Consolas, monospace" font-weight="600" font-size="14" fill="#a0c8ff" style="text-shadow: 0 0 3px #1e3a72;" pointer-events="none">{label}</text>'''

svg += '</svg>'

with open(output, "w") as f:
    f.write(svg)

print(f"Advanced Cyber Radar SVG saved to {output}")


