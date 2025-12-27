from pathlib import Path
import random

# Ensure assets folder exists
Path("assets").mkdir(exist_ok=True)

# Threat categories (columns)
threats = ["Phishing", "Malware", "Lateral Movement", "Exploits", "Ransomware", "Command & Control"]

# Systems or areas monitored (rows)
systems = ["Endpoints", "Network", "Cloud", "Identity", "Apps", "Databases"]

cell_size = 80
padding = 20

width = cell_size * len(threats) + padding*2
height = cell_size * len(systems) + padding*2

svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
<style>
.text {{ font: bold 12px sans-serif; fill: #222; }}
.cell {{ stroke: #444; stroke-width: 2; }}
</style>
'''

# Draw cells and labels
for row_idx, system in enumerate(systems):
    for col_idx, threat in enumerate(threats):
        x = padding + col_idx*cell_size
        y = padding + row_idx*cell_size
        svg += f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="#eee" class="cell"/>\n'
        
        # Animated threat "alert" circles
        # Randomize animation delay for dynamic feel
        delay = random.uniform(0, 2)
        svg += f'''
<circle cx="{x + cell_size/2}" cy="{y + cell_size/2}" r="0" fill="#ff4500">
    <animate attributeName="r" values="0;15;0" dur="1.5s" repeatCount="indefinite" begin="{delay}s"/>
    <animate attributeName="opacity" values="0;1;0" dur="1.5s" repeatCount="indefinite" begin="{delay}s"/>
</circle>
'''

# Add column labels (threats)
for col_idx, threat in enumerate(threats):
    x = padding + col_idx*cell_size + cell_size/2
    y = padding - 5
    svg += f'<text x="{x}" y="{y}" class="text" text-anchor="middle">{threat}</text>\n'

# Add row labels (systems)
for row_idx, system in enumerate(systems):
    x = padding - 5
    y = padding + row_idx*cell_size + cell_size/2 + 4
    svg += f'<text x="{x}" y="{y}" class="text" text-anchor="end">{system}</text>\n'

svg += "</svg>"

# Save SVG
with open("assets/threat_matrix.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("Animated Cyber Threat Matrix generated at assets/threat_matrix.svg")
