from pathlib import Path

Path("assets").mkdir(exist_ok=True)

stages = ["Detection", "Triage", "Investigation", "Containment", "Reporting", "Remediation"]
num_stages = len(stages)
width = 700
height = 150
box_width = 100
box_height = 50
padding = 20
gap = (width - 2*padding - num_stages*box_width) / (num_stages - 1)

svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n'
svg += '<style>.stage { fill: #0078d7; stroke: #333; stroke-width: 2; } .label { font: bold 12px sans-serif; fill: white; }</style>\n'

for i, stage in enumerate(stages):
    x = padding + i*(box_width + gap)
    y = (height - box_height)/2
    # Pulse animation for each stage
    delay = i * 0.5
    svg += f'''
<rect x="{x}" y="{y}" width="{box_width}" height="{box_height}" rx="8" ry="8" class="stage">
  <animate attributeName="fill" values="#0078d7;#00c0ff;#0078d7" dur="2s" repeatCount="indefinite" begin="{delay}s"/>
</rect>
<text x="{x + box_width/2}" y="{y + box_height/2 + 5}" class="label" text-anchor="middle">{stage}</text>
'''

# Draw arrows between stages
for i in range(num_stages-1):
    x1 = padding + (i+0.5)*(box_width + gap)
    y1 = height/2
    x2 = x1 + gap
    y2 = y1
    svg += f'<line x1="{x1+box_width/2}" y1="{y1}" x2="{x2-box_width/2}" y2="{y2}" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>\n'

# Define arrowhead
svg += '''
<defs>
<marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto" markerUnits="strokeWidth">
<path d="M0,0 L0,6 L9,3 z" fill="#333" />
</marker>
</defs>
'''

svg += "</svg>"

with open("assets/incident_flow.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("Incident lifecycle SVG generated at assets/incident_flow.svg")

