import random
import os

# Output file path
output_path = os.path.join("assets", "cyber_heatmap_live.svg")

# Hosts with mock positions
hosts = [
    {"name": "HostA", "x": 100, "y": 80},
    {"name": "Server42", "x": 250, "y": 180},
    {"name": "Workstation12", "x": 400, "y": 120},
    {"name": "Firewall", "x": 150, "y": 300},
    {"name": "DBServer", "x": 350, "y": 250},
]

# Assign random activity
for host in hosts:
    host["activity"] = random.randint(0, 100)  # intensity 0-100

# Create SVG
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400">
<rect width="600" height="400" fill="#0a0f1a"/>
'''

for host in hosts:
    intensity = host["activity"] / 100
    radius = 6 + 4 * intensity
    opacity = 0.5 + 0.5 * intensity
    svg_content += f'''
    <circle cx="{host["x"]}" cy="{host["y"]}" r="{radius}" fill="#4effff" opacity="{opacity}">
        <animate attributeName="r" values="{radius};{radius+4};{radius}" dur="3s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="{opacity};1;{opacity}" dur="3s" repeatCount="indefinite"/>
    </circle>
    <text x="{host["x"] + 10}" y="{host["y"] + 5}" font-family="Consolas, monospace" font-size="12" fill="#a0c8ff">{host["name"]}</text>
    '''

svg_content += "</svg>"

# Write to file
with open(output_path, "w") as f:
    f.write(svg_content)

print(f"Cyber heatmap generated: {output_path}")
