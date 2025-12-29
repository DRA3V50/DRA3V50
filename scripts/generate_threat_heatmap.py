import os
import random

# Make sure assets folder exists
os.makedirs("assets", exist_ok=True)

# Hosts/data points for your heatmap
hosts = [
    {"name": "HostA", "x": 100, "y": 50},
    {"name": "Server42", "x": 200, "y": 120},
    {"name": "Workstation12", "x": 300, "y": 200},
    {"name": "Router1", "x": 400, "y": 80},
    {"name": "DBServer", "x": 500, "y": 150},
]

# Generate random "activity" for each host
for host in hosts:
    # assign intensity 0-100
    host["activity"] = random.randint(0, 100)

# Create SVG content
svg_header = """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400">
  <rect width="600" height="400" fill="#0a0f1a"/>"""

svg_footer = "</svg>"

host_circles = ""

for host in hosts:
    intensity = host["activity"]
    radius = 6 + intensity * 0.05  # scale radius by activity
    opacity = 0.5 + (intensity / 200)  # scale opacity 0.5-1
    color = "#ff4e4e" if intensity > 70 else "#4effff"
    
    host_circles += f"""
  <circle cx="{host['x']}" cy="{host['y']}" r="{radius}" fill="{color}">
    <animate attributeName="r" values="{radius};{radius+4};{radius}" dur="3s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="{opacity};1;{opacity}" dur="3s" repeatCount="indefinite"/>
  </circle>
  <text x="{host['x'] + 10}" y="{host['y'] + 5}" font-family="Consolas, monospace" font-size="12" fill="#a0c8ff">{host['name']}</text>"""

# Combine everything
svg_content = svg_header + host_circles + svg_footer

# Write SVG to file
output_path = "assets/cyber_heatmap_live.svg"
with open(output_path, "w") as f:
    f.write(svg_content)

print(f"SVG heatmap generated: {output_path}")

