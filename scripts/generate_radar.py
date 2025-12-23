import json
from pathlib import Path

DATA_FILE = Path("scripts/data.json")
OUTPUT_FILE = Path("assets/blue-team-radar.svg")

data = json.loads(DATA_FILE.read_text())

labels = data["labels"]
values = data["values"]

cx, cy = 200, 200
radius = 120

def escape(text):
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
    )

svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="400"
     height="400"
     viewBox="0 0 400 400"
     role="img"
     aria-label="Blue Team Capability Radar">

<rect width="100%" height="100%" fill="#0d1117"/>

<circle cx="200" cy="200" r="120" fill="none" stroke="#30363d"/>
<circle cx="200" cy="200" r="80" fill="none" stroke="#30363d"/>
<circle cx="200" cy="200" r="40" fill="none" stroke="#30363d"/>

<g stroke="#30363d">
'''

import math
points = []

for i, value in enumerate(values):
    angle = (2 * math.pi / len(values)) * i - math.pi / 2
    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)
    svg += f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" />\n'

    px = cx + (radius * value) * math.cos(angle)
    py = cy + (radius * value) * math.sin(angle)
    points.append(f"{px},{py}")

svg += "</g>\n"

svg += f'''
<polygon points="{' '.join(points)}"
         fill="rgba(88,166,255,0.35)"
         stroke="#58a6ff"
         stroke-width="2">
  <animateTransform
      attributeName="transform"
      type="rotate"
      from="0 200 200"
      to="360 200 200"
      dur="40s"
      repeatCount="indefinite"/>
</polygon>
'''

for i, label in enumerate(labels):
    angle = (2 * math.pi / len(labels)) * i - math.pi / 2
    lx = cx + 150 * math.cos(angle)*

