from pathlib import Path
import json
import math

# Ensure assets folder exists
Path("assets").mkdir(exist_ok=True)

# Load MITRE coverage data
try:
    with open("radar-config.json") as f:
        coverage_data = json.load(f).get("mitre_coverage", {})
except FileNotFoundError:
    coverage_data = {
        "Initial Access": 70,
        "Execution": 50,
        "Persistence": 80,
        "Privilege Escalation": 60,
        "Defense Evasion": 40,
        "Credential Access": 90
    }

# SVG parameters
width, height = 500, 500
cx, cy = width//2, height//2
radius_step = 50
svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
<style>
.text {{ font: bold 12px sans-serif; fill: #222; }}
</style>
'''

# Function to generate a circle arc path
def arc_path(cx, cy, r, percent):
    from math import sin, cos, pi
    start_angle = -pi/2  # start at top
    end_angle = start_angle + 2*pi*(percent/100)
    x1 = cx + r * cos(start_angle)
    y1 = cy + r * sin(start_angle)
    x2 = cx + r * cos(end_angle)
    y2 = cy + r * sin(end_angle)
    large_arc = 1 if percent > 50 else 0
    return f'M {x1} {y1} A {r} {r} 0 {large_arc} 1 {x2} {y2}'

# Draw arcs
for i, (tactic, percent) in enumerate(coverage_data.items()):
    r = radius_step * (i+1)
    # Background arc (full gray)
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ccc" stroke-width="12"/>\n'
    # Coverage arc
    path = arc_path(cx, cy, r, percent)
    svg += f'<path d="{path}" fill="none" stroke="#1e90ff" stroke-width="12" stroke-linecap="round"/>\n'
    # Label
    svg += f'<text x="{cx}" y="{cy - r - 5}" class="text" text-anchor="middle">{tactic} ({percent}%)</text>\n'

svg += "</svg>"

with open("assets/mitre.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("Static MITRE coverage SVG (GitHub-compatible) generated at assets/mitre.svg")
