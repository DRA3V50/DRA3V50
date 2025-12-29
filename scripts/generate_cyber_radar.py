import random
from math import cos, sin, radians
from pathlib import Path

# Output and dimensions
WIDTH, HEIGHT = 500, 500
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
RADAR_RADIUS = 220
output = Path("assets/cyber_radar_static.svg")
output.parent.mkdir(parents=True, exist_ok=True)

# Example MITRE ATT&CK-style data points: (label, tactic, angle, distance)
data_points = [
    ("Phishing", "Initial Access", 20, 180),
    ("Brute Force", "Credential Access", 70, 160),
    ("Lateral Movement", "Lateral Movement", 120, 200),
    ("Exfiltration", "Exfiltration", 200, 170),
    ("Command & Control", "Command & Control", 300, 190),
    ("Defense Evasion", "Defense Evasion", 270, 140),
]

# Color mapping by tactic
tactic_colors = {
    "Initial Access": "#ff5c5c",
    "Credential Access": "#ffb14c",
    "Lateral Movement": "#5cb3ff",
    "Exfiltration": "#ff4dff",
    "Command & Control": "#2fffd3",
    "Defense Evasion": "#ffd700",
}

# Start SVG
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <!-- Glow filter -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#5cb3ff" flood-opacity="0.7"/>
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
    svg += f'<circle cx="{CENTER_X}" cy="{CENTER_Y}" r="{r}" fill="none" stroke="#2f6fed" stroke-width="1" opacity="0.3"/>\n'

# Draw spokes every 30 degrees
for angle in range(0, 360, 30):
    rad = radians(angle)
    x = CENTER_X + RADAR_RADIUS * cos(rad)
    y = CENTER_Y + RADAR_RADIUS * sin(rad)
    svg += f'<line x1="{CENTER_X}" y1="{CENTER_Y}" x2="{x}" y2="{y}" stroke="#2f6fed" stroke-width="1" opacity="0.15"/>\n'

# Draw sweeping radar beam as static semi-transparent sector
svg += f'''
<path d="M{CENTER_X},{CENTER_Y} L{CENTER_X + RADAR_RADIUS}, {CENTER_Y} 
         A{RADAR_RADIUS},{RADAR_RADIUS} 0 0,1 {CENTER_X + int(RADAR_RADIUS*0.7)}, {CENTER_Y - int(RADAR_RADIUS*0.7)} Z"
      fill="url(#sweepGrad)" filter="url(#glow)"/>
'''

# Draw data points with glow + pulsing simulation + MITRE tactic color
for label, tactic, angle_deg, dist in data_points:
    rad = radians(angle_deg)
    x = CENTER_X + dist * cos(rad)
    y = CENTER_Y + dist * sin(rad)
    r_dot = random.randint(6, 10)
    fill_color = tactic_colors.get(tactic, "#5cb3ff")

    # Glow / pulse circle behind
    svg += f'<circle cx="{x}" cy="{y}" r="{r_dot + 4}" fill="{fill_color}" opacity="0.15"/>\n'

    # Main dot
    svg += f'<circle cx="{x}" cy="{y}" r="{r_dot}" fill="{fill_color}" filter="url(#glow)"/>\n'

    # Label
    svg += f'<text x="{x + 12}" y="{y + 5}" font-family="Consolas, monospace" font-size="12" fill="#a0c8ff">{label}</text>\n'

# End SVG
svg += '</svg>'

# Save
with open(output, "w") as f:
    f.write(svg)

print(f"Cyber radar SVG with MITRE-style points saved to {output}")
