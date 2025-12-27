from pathlib import Path
import math

# Ensure assets folder exists
Path("assets").mkdir(exist_ok=True)

# SOC Skills and proficiency %
skills = {
    "SOC Ops": 90,
    "Incident Response": 85,
    "SIEM": 80,
    "EDR": 70,
    "Threat Intel": 75,
    "SOAR": 65
}

# Alert stages
stages = ["Alert", "Triage", "Investigation", "Resolution"]

width, height = 600, 600
cx, cy = width//2, height//2
radius_step = 50

svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
<style>
.text {{ font: bold 12px sans-serif; fill: #222; }}
.stage {{ font: bold 14px sans-serif; fill: #000; }}
</style>
'''

# --- Draw Skill Rings ---
for i, (skill, percent) in enumerate(skills.items()):
    r = radius_step * (i + 1)
    circumference = 2 * math.pi * r
    fill_offset = circumference * (1 - percent/100)
    
    # Background circle
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ccc" stroke-width="10"/>\n'
    
    # Animated proficiency arc
    svg += f'''
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1e90ff" stroke-width="10"
        stroke-dasharray="{circumference}" stroke-dashoffset="{circumference}">
    <animate attributeName="stroke-dashoffset" from="{circumference}" to="{fill_offset}" dur="1.5s" fill="freeze"/>
</circle>
'''
    # Pulsing glow overlay
    svg += f'''
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1e90ff" stroke-width="10" stroke-dasharray="{circumference}" stroke-dashoffset="0" opacity="0.3">
    <animate attributeName="opacity" values="0.3;0.6;0.3" dur="2s" repeatCount="indefinite"/>
</circle>
'''
    # Skill label
    svg += f'<text x="{cx}" y="{cy - r - 5}" class="text" text-anchor="middle">{skill} ({percent}%)</text>\n'

# --- Draw SOC Stages ---
stage_radius = radius_step * (len(skills)+1)
angle_step = 360 / len(stages)
for i, stage in enumerate(stages):
    angle = math.radians(i*angle_step - 90)  # start top
    x = cx + stage_radius * math.cos(angle)
    y = cy + stage_radius * math.sin(angle)
    svg += f'<text x="{x}" y="{y}" class="stage" text-anchor="middle">{stage}</text>\n'

# --- Animate Alerts moving between stages ---
for i, stage in enumerate(stages[:-1]):
    r1 = stage_radius
    r2 = stage_radius
    start_angle = math.radians(i*angle_step - 90)
    end_angle = math.radians((i+1)*angle_step - 90)
    # Simple linear path for demo
    x1 = cx + r1 * math.cos(start_angle)
    y1 = cy + r1 * math.sin(start_angle)
    x2 = cx + r2 * math.cos(end_angle)
    y2 = cy + r2 * math.sin(end_angle)
    
    svg += f'''
<circle r="6" fill="#ff4500">
  <animateMotion dur="4s" repeatCount="indefinite">
    <mpath>
      <path d="M {x1} {y1} L {x2} {y2}"/>
    </mpath>
  </animateMotion>
</circle>
'''

# --- Optional MITRE-style outer blip ---
outer_r = stage_radius + 40
svg += f'''
<circle r="5" fill="#32cd32">
  <animateMotion dur="6s" repeatCount="indefinite">
    <mpath>
      <path d="M {cx} {cy - outer_r} A {outer_r} {outer_r} 0 1 1 {cx-0.01} {cy - outer_r}"/>
    </mpath>
  </animateMotion>
</circle>
'''

svg += "</svg>"

# Save file
with open("assets/soc_dashboard.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("Animated SOC Dashboard SVG generated at assets/soc_dashboard.svg")
