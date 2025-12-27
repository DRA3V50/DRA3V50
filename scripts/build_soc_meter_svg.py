from pathlib import Path

Path("assets").mkdir(exist_ok=True)

# SOC areas and target coverage/activity levels
areas = {
    "SIEM": 0.9,
    "Endpoint": 0.7,
    "Cloud": 0.6,
    "IR": 0.8
}

width = 500
height = 200
center_y = 120
center_x_start = 80
gap_x = 120
radius = 40

svg_elements = []

# SVG header
svg_elements.append(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')
svg_elements.append('<style> text { fill:white; font-family:Arial, sans-serif; font-size:14px;} .bg { fill:#323232;} .fill { fill:#0078FF;} </style>')

for i, (area, value) in enumerate(areas.items()):
    cx = center_x_start + i*gap_x
    cy = center_y

    # Background circle
    svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" class="bg"/>')

    # Animated fill arc using stroke-dasharray trick
    circumference = 2 * 3.1416 * radius
    fill_length = value * circumference
    svg_elements.append(f'''
    <circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#0078FF" stroke-width="8"
        stroke-dasharray="0,{circumference}">
        <animate attributeName="stroke-dasharray" from="0,{circumference}" to="{fill_length},{circumference}" dur="2s" fill="freeze"/>
    </circle>
    ''')

    # Label
    svg_elements.append(f'<text x="{cx}" y="{cy+radius+20}" text-anchor="middle">{area}</text>')

svg_elements.append('</svg>')

# Save SVG
svg_path = "assets/soc_activity_meter.svg"
with open(svg_path, "w") as f:
    f.write("\n".join(svg_elements))

print(f"Animated SOC Activity Meter SVG generated at {svg_path}")


