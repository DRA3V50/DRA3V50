import random
import os

# Make sure assets folder exists
os.makedirs("assets", exist_ok=True)

# Example hosts/threats
hosts = [
    {"name": "HostA", "x": 100, "y": 80},
    {"name": "Server42", "x": 300, "y": 200},
    {"name": "DB01", "x": 500, "y": 120},
    {"name": "Firewall", "x": 400, "y": 300},
]

# Start SVG
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400">
<rect width="600" height="400" fill="#0a0f1a"/>
'''

# Add animated points
for host in hosts:
    intensity = random.randint(5, 15)  # size of pulse
    color = "#ff4e4e" if random.random() < 0.5 else "#4effff"
    svg_content += f'''
    <circle cx="{host['x']}" cy="{host['y']}" r="{intensity}" fill="{color}" fill-opacity="0.6">
        <animate attributeName="r" values="{intensity};{intensity+5};{intensity}" dur="2s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="{host['x']+10}" y="{host['y']+5}" font-family="Consolas, monospace" font-size="12" fill="#a0c8ff">{host['name']}</text>
    '''

# Finish SVG
svg_content += "</svg>"

# Write to assets folder
with open("assets/cyber_heatmap_live.svg", "w") as f:
    f.write(svg_content)

print("✅ SVG generated successfully!")
