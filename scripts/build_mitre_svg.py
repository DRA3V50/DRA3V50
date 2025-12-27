from pathlib import Path
import json
import math

# Ensure assets folder exists
Path("assets").mkdir(exist_ok=True)

# Load MITRE coverage data
# Example structure: {"Initial Access": 70, "Execution": 50, "Persistence": 80, ...}
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
cx, cy = width//2, height//2
radius_step = 50
angle_step = 360 / max(len(coverage_data), 1)

# SVG header
svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
<style>
.text {{ font: bold 12px sans-serif; fill: #222; }}
</style>
'''

# Generate arcs and animations
for i, (tactic, percent) in enumerate(coverage_data.items()):
    r = radius_step * (i + 1)
    circumference = 2 * math.pi * r
    offset = circumference
    fill_offset = circumference * (1 - percent / 100)
    # Background circle
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ccc" stroke-width="12"/>\n'
    # Animated coverage circle
    svg += f'''
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1e90ff" stroke-width="12"
        stroke-dasharray="{circumference}" stroke-dashoffset="{circumference}">
    <animate attributeName="stroke-dashoffset" from="{circumference}" to="{fill_offset}" dur="2s" fill="freeze"/>
</circle>
'''
    # Add tactic label
    svg += f'<text x="{cx}" y="{cy - r - 5}" class="text" text-anchor="middle">{tactic}</text>\n'

# Optional: moving blip along outermost arc
if coverage_data:
    outer_r = radius_step * len(coverage_data)
    circumference = 2 * math.pi * outer_r
    svg += f'''
<circle cx="{cx}" cy="{cy}" r="6" fill="#ff4500">
    <animateMotion dur="4s" repeatCount="indefinite" rotate="auto">
        <mpath>
            <path d="M {cx} {cy - outer_r} A {outer_r} {outer_r} 0 1 1 {cx-0.01} {cy - outer_r}"/>
        </mpath>
    </animateMotion>
</circle>
'''

# SVG footer
svg += "</svg>"

# Write to file
with open("assets/mitre.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("Animated MITRE coverage SVG generated at assets/mitre.svg")
