from pathlib import Path
import json
import math

# Load MITRE coverage data
with open("radar-config.json") as f:
    data = json.load(f)

# Example: list of coverage percentages per tactic
# Replace with real data parsing
tactics = data.get("mitre_coverage", {"Initial Access": 70, "Execution": 50, "Persistence": 80})

# Create assets folder
Path("assets").mkdir(exist_ok=True)

# SVG header
svg_header = """<svg width="500" height="500" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
<style>
.text { font: bold 14px sans-serif; }
</style>
"""

# Draw arcs for each tactic
svg_arcs = ""
cx, cy = 250, 250
radius_step = 60
angle_step = 360 / len(tactics)

for i, (tactic, percent) in enumerate(tactics.items()):
    r = radius_step * (i + 1)
    angle = angle_step * i
    # SVG uses radians for math
    svg_arcs += f"""
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ccc" stroke-width="20" />
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#00f" stroke-width="20"
          stroke-dasharray="{2*math.pi*r}" stroke-dashoffset="{2*math.pi*r}">
    <animate attributeName="stroke-dashoffset" from="{2*math.pi*r}" to="{2*math.pi*r*(1 - percent/100)}"
             dur="2s" fill="freeze" />
  </circle>
  <text x="{cx}" y="{cy - r}" class="text" text-anchor="middle">{tactic}</text>
"""

# SVG footer
svg_footer = "</svg>"

# Write SVG file
with open("assets/mitre.svg", "w", encoding="utf-8") as f:
    f.write(svg_header + svg_arcs + svg_footer)

print("MITRE coverage SVG generated at assets/mitre.svg")
