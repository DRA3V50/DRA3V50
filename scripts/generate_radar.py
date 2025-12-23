import json
import math
from pathlib import Path

DATA_FILE = Path("scripts/data.json")
OUTPUT_FILE = Path("assets/blue-team-radar.svg")

data = json.loads(DATA_FILE.read_text())
labels = data["labels"]
values = data["values"]

cx, cy = 200, 200
radius = 120
arc_width = 10
num_axes = len(values)

def escape(text):
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
    )

# Start SVG
svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="400"
     height="400"
     viewBox="0 0 400 400"
     role="img"
     aria-label="Blue Team Capability Radar">

<rect width="100%" height="100%" fill="#0d1117"/>

<circle cx="{cx}" cy="{cy}" r="120" fill="none" stroke="#30363d"/>
<circle cx="{cx}" cy="{cy}" r="80" fill="none" stroke="#30363d"/>
<circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="#30363d"/>

<g stroke="#30363d">
'''

# Axis lines
for i in range(num_axes):
    angle = (2 * math.pi / num_axes) * i - math.pi / 2
    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)
    svg += f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" />\n'

svg += "</g>\n"

# Start CSS for animation
svg += "<style>\n"
svg += ".pulse { stroke-opacity: 0.6; animation: pulse 2s infinite alternate; }\n"
svg += "@keyframes pulse { from { stroke-opacity: 0.6; } to { stroke-opacity: 1; } }\n"
svg += "</style>\n"

# Signal arcs using CSS animation
for i, value in enumerate(values):
    start_angle = (2 * math.pi / num_axes) * i - math.pi / 2
    arc_angle = value * (2 * math.pi / num_axes)
    end_angle = start_angle + arc_angle

    x1 = cx + radius * math.cos(start_angle)
    y1 = cy + radius * math.sin(start_angle)
    x2 = cx + radius * math.cos(end_angle)
    y2 = cy + radius * math.sin(end_angle)

    delay = i * 0.3  # optional desync

    svg += f'''
<path d="M {x1:.2f},{y1:.2f} A {radius},{radius} 0 0 1 {x2:.2f},{y2:.2f}"
      stroke="rgba(88,166,255,0.85)"
      stroke-width="{arc_width}"
      fill="none"
      stroke-linecap="round"
      class="pulse"
      style="animation-delay:{delay}s"/>
'''

# Labels
for i, label in enumerate(labels):
    angle = (2 * math.pi / num_axes) * i - math.pi / 2
    lx = cx + 150 * math.cos(angle)
    ly = cy + 150 * math.sin(angle)

    svg += f'''
<text x="{lx}" y="{ly}"
      fill="#c9d1d9"
      font-size="11"
      text-anchor="middle">
  {escape(label)}
</text>
'''

svg += "</svg>"

OUTPUT_FILE.write_text(svg, encoding="utf-8")


