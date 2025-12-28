from pathlib import Path
import random
from math import cos, sin, radians

WIDTH, HEIGHT = 400, 400
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
RADAR_RADIUS = 180

output = Path("assets/cyber_radar.svg")
output.parent.mkdir(parents=True, exist_ok=True)

# Build SVG content as a string
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">
  <rect width="{WIDTH}" height="{HEIGHT}" fill="#0a0f1a"/>
'''

# Radar circles
for r in range(40, RADAR_RADIUS+1, 40):
    svg += f'  <circle cx="{CENTER_X}" cy="{CENTER_Y}" r="{r}" fill="none" stroke="#2f6fed" stroke-width="1" opacity="0.3"/>\n'

# Radar lines
for angle in range(0, 360, 45):
    rad = radians(angle)
    x = CENTER_X + RADAR_RADIUS * cos(rad)
    y = CENTER_Y + RADAR_RADIUS * sin(rad)
    svg += f'  <line x1="{CENTER_X}" y1="{CENTER_Y}" x2="{x}" y2="{y}" stroke="#2f6fed" stroke-width="1" opacity="0.3"/>\n'

# Sweep
svg += f'''  <defs>
    <linearGradient id="sweepGradient" gradientTransform="rotate(45)">
      <stop offset="0%" stop-color="#2f6fed"/>
      <stop offset="100%" stop-color="#2f6fed" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <path d="M{CENTER_X},{CENTER_Y} L{CENTER_X+RADAR_RADIUS},{CENTER_Y} A{RADAR_RADIUS},{RADAR_RADIUS} 0 0,1 {CENTER_X+int(RADAR_RADIUS*0.7)},{CENTER_Y-int(RADAR_RADIUS*0.7)} Z"
        fill="url(#sweepGradient)" opacity="0.25">
    <animateTransform attributeName="transform" type="rotate" from="0 {CENTER_X} {CENTER_Y}" to="360 {CENTER_X} {CENTER_Y}" dur="6s" repeatCount="indefinite"/>
  </path>
'''

# Pulsing threat blips
for _ in range(10):
    angle = random.uniform(0, 360)
    distance = random.uniform(20, RADAR_RADIUS)
    rad = radians(angle)
    x = CENTER_X + distance * cos(rad)
    y = CENTER_Y + distance * sin(rad)
    dur = round(random.uniform(2,4), 2)
    begin = round(random.uniform(0,4), 2)
    svg += f'''  <circle cx="{x}" cy="{y}" r="6" fill="#5cb3ff" opacity="0.6">
    <animate attributeName="r" values="6;10;6" dur="{dur}s" repeatCount="indefinite" begin="{begin}s"/>
    <animate attributeName="opacity" values="0.6;1;0.6" dur="{dur}s" repeatCount="indefinite" begin="{begin}s"/>
  </circle>\n'''

svg += '</svg>'

# Write file
with open(output, "w") as f:
    f.write(svg)

print("Generated assets/cyber_radar.svg successfully!")

