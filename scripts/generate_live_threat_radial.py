import random
import os
import math

os.makedirs("assets", exist_ok=True)

WIDTH = 200
HEIGHT = 150
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT
RADIUS = 60

threats = [
    {"name": "Ransomware", "severity": "Critical"},
    {"name": "Phishing", "severity": "High"},
    {"name": "Vulnerability", "severity": "Medium"}
]

severity_color = {
    "Critical": "#ff4e4e",
    "High": "#ffb74e",
    "Medium": "#4effff"
}

# Random counts
for t in threats:
    t["count"] = random.randint(1, 25)

# Generate SVG
with open("assets/live_threat_radial.svg", "w") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}">\n')
    f.write(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#0a0f1a"/>\n')
    f.write(f'<text x="10" y="15" font-family="Consolas, monospace" font-size="12" fill="#a0c8ff">Threat Radial</text>\n')

    start_angle = -90
    for t in threats:
        # Arc length proportional to count
        end_angle = start_angle + (t["count"] / 25) * 180  # semi-circle
        # Convert to SVG path coordinates
        x1 = CENTER_X + RADIUS * math.cos(math.radians(start_angle))
        y1 = CENTER_Y + RADIUS * math.sin(math.radians(start_angle))
        x2 = CENTER_X + RADIUS * math.cos(math.radians(end_angle))
        y2 = CENTER_Y + RADIUS * math.sin(math.radians(end_angle))
        large_arc = 1 if end_angle - start_angle > 180 else 0

        path = f'M {CENTER_X},{CENTER_Y} L {x1},{y1} A {RADIUS},{RADIUS} 0 {large_arc} 1 {x2},{y2} Z'
        f.write(f'<path d="{path}" fill="{severity_color[t["severity"]]}">\n')
        f.write(f'<animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite"/>\n')
        f.write('</path>\n')
        start_angle = end_angle + 5  # small gap between arcs

    f.write('</svg>')

print("Live Threat Radial SVG generated successfully!")
