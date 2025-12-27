from pathlib import Path
import random

Path("assets").mkdir(exist_ok=True)

width = 600
height = 400
num_alerts = 8

svg_elements = []

# SVG header
svg_elements.append(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')
svg_elements.append('<style> .alert { fill: #0078FF; } .investigate { fill: #FFC107; } .resolved { fill: #4CAF50; } </style>')

for i in range(num_alerts):
    # Random start positions
    x = 50 + i*60
    y = 50

    # Alert circle
    svg_elements.append(f'''
    <circle cx="{x}" cy="{y}" r="15" class="alert">
      <animate attributeName="cy" values="{y};{y+300};{y+150}" dur="4s" repeatCount="indefinite"/>
      <animate attributeName="fill" values="#0078FF;#FFC107;#4CAF50" dur="4s" repeatCount="indefinite"/>
    </circle>
    ''')

# Optional labels
svg_elements.append(f'<text x="{width/2}" y="20" fill="white" font-family="Arial" font-size="18" text-anchor="middle">SOC Alert Flow</text>')

svg_elements.append('</svg>')

# Save SVG
svg_path = "assets/alert_flow.svg"
with open(svg_path, "w") as f:
    f.write("\n".join(svg_elements))

print(f"Animated Alert Flow SVG generated at {svg_path}")

