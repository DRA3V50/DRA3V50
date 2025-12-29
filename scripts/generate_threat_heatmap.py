import random
import os

# Threat categories
categories = [
    "Initial Access", "Execution", "Persistence", "Privilege Escalation",
    "Defense Evasion", "Credential Access", "Discovery",
    "Lateral Movement", "Exfiltration", "Impact"
]

# Generate random threat levels (0-100)
threat_levels = [random.randint(0, 100) for _ in categories]

# Map threat level to color
def get_color(value):
    if value > 70: return "#ff4e4e"
    elif value > 40: return "#f5a623"
    else: return "#4effff"

# SVG output
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="300" viewBox="0 0 600 300">\n'
svg += '<rect width="600" height="300" fill="#0a0f1a"/>\n'

bar_width = 50
spacing = 10
x = 10

for cat, level in zip(categories, threat_levels):
    color = get_color(level)
    bar_height = level * 2  # scale to fit 0-200px
    y = 250 - bar_height
    svg += f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{color}" rx="4"/>\n'
    svg += f'<text x="{x}" y="265" font-size="10" fill="#a0c8ff" font-family="monospace">{cat}</text>\n'
    x += bar_width + spacing

svg += '</svg>'

# Ensure assets folder exists
os.makedirs("assets", exist_ok=True)

# Write SVG
with open("assets/cyber_heatmap_live.svg", "w") as f:
    f.write(svg)

print("Generated cyber_heatmap_live.svg")
