import random
from datetime import datetime

# SVG output file
output_file = "assets/cyber_radar_live.svg"

# MITRE ATT&CK tactics (cyber kill chain style)
tactics = [
    "Initial Access", "Execution", "Persistence", "Privilege Escalation",
    "Defense Evasion", "Credential Access", "Discovery", "Lateral Movement",
    "Exfiltration", "Impact"
]

# SVG settings
width = 600
height = 400
line_spacing = 30

# Generate random values to simulate live activity
def generate_points(y):
    points = []
    for x in range(0, width+1, 50):
        dy = random.randint(-10, 10)
        points.append((x, y + dy))
    return points

# Convert points to SVG path string
def points_to_path(points):
    return "M" + " L".join(f"{x},{y}" for x, y in points)

# Start building SVG
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
svg += f'  <rect width="{width}" height="{height}" fill="#0a0f1a"/>\n'
svg += '  <defs>\n'
svg += '    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">\n'
svg += '      <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#4effff" flood-opacity="0.8"/>\n'
svg += '    </filter>\n'
svg += '    <linearGradient id="lineGrad" x1="0" y1="0" x2="0" y2="1">\n'
svg += '      <stop offset="0%" stop-color="#2f6fed"/>\n'
svg += '      <stop offset="100%" stop-color="#5cb3ff"/>\n'
svg += '    </linearGradient>\n'
svg += '  </defs>\n'

# Horizontal reference lines
for i in range(len(tactics)):
    y = 50 + i * line_spacing
    svg += f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#1e2a45" stroke-width="1"/>\n'

# Animated paths for each tactic
for i, tactic in enumerate(tactics):
    y_base = 50 + i * line_spacing
    points1 = generate_points(y_base)
    points2 = generate_points(y_base)
    path_values = f"{points_to_path(points1)}; {points_to_path(points2)}"
    svg += f'<path d="{points_to_path(points1)}" fill="none" stroke="url(#lineGrad)" stroke-width="3" filter="url(#glow)">\n'
    svg += f'  <animate attributeName="d" values="{path_values}" dur="{4+random.random()*3:.2f}s" repeatCount="indefinite"/>\n'
    svg += '</path>\n'
    svg += f'<text x="10" y="{y_base-5}" font-family="Consolas, monospace" font-size="12" fill="#a0c8ff">{tactic}</text>\n'

# Optional subtle “eye” monitoring circle
svg += f'<circle cx="{width-50}" cy="{height//2}" r="20" fill="none" stroke="#5cb3ff" stroke-width="2">\n'
svg += f'  <animate attributeName="r" values="18;22;18" dur="3s" repeatCount="indefinite"/>\n'
svg += '</circle>\n'

# Footer timestamp
svg += f'<text x="10" y="{height-10}" font-family="Consolas, monospace" font-size="10" fill="#888">{datetime.utcnow().isoformat()} UTC</text>\n'
svg += '</svg>'

# Write to file
with open(output_file, "w") as f:
    f.write(svg)

print(f"Generated {output_file}")

