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
    # fallback example data
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
cx, cy = width // 2, height // 2
radius_step = 50

# SVG header
svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
<style>
.text {{ font: bold 12px sans-serif; fill: #222; }}
</style>
'''

# Generate arcs
for i, (tactic, percent) in enumerate(coverage_data.items()):
    r = radius_step * (i + 1)
    circumference = 2 * math.pi * r
    fill_offset = circumference * (1 - percent / 100)

    # Background circle (gray)
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ccc" stroke-width="12"/>\n'

    # Filled circle for coverage
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1e90ff" stroke-width="12" ' \
           f'stroke-dasharray="{circumference}" stroke-dashoffset="{fill_offset}"/>\n'

    # Add tactic label above the arc
    svg += f'<text x="{cx}" y="{cy - r - 5}" class="text" text-anchor="middle">{tactic} ({percent}%)</text>\n'

# SVG footer
svg += "</svg>"

# Write SVG file
with open("assets/mitre.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("Static MITRE coverage SVG generated at assets/mitre.svg")
