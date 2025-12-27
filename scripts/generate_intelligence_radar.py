from datetime import datetime
import random
import math

points = [
    ("Endpoint Detection", random.uniform(0.5, 1.0)),
    ("SIEM Engineering", random.uniform(0.5, 1.0)),
    ("Anomaly Detection", random.uniform(0.5, 1.0)),
    ("OSINT & Logs", random.uniform(0.5, 1.0)),
    ("SOAR & Automation", random.uniform(0.5, 1.0)),
    ("SOC Operations", random.uniform(0.5, 1.0)),
]

def polar_to_cartesian(cx, cy, angle_deg, radius):
    angle_rad = math.radians(angle_deg - 90)
    x = cx + radius * math.cos(angle_rad)
    y = cy + radius * math.sin(angle_rad)
    return x, y

cx, cy = 150, 150
max_radius = 120
angle_step = 360 / len(points)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">
  <rect width="100%" height="100%" fill="#0b0f14"/>
  <circle cx="{cx}" cy="{cy}" r="{max_radius}" stroke="#00ffcc" stroke-width="2" fill="none"/>
  <circle cx="{cx}" cy="{cy}" r="{max_radius*0.66}" stroke="#008877" stroke-width="1" fill="none" opacity="0.3"/>
  <circle cx="{cx}" cy="{cy}" r="{max_radius*0.33}" stroke="#004433" stroke-width="1" fill="none" opacity="0.2"/>
  <line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - max_radius}" stroke="#00ffcc" stroke-width="2">
    <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="5s" repeatCount="indefinite"/>
  </line>
  <circle cx="{cx}" cy="{cy}" r="5" fill="#00ffcc"/>
'''

for i, (label, dist_ratio) in enumerate(points):
    angle = i * angle_step
    x, y = polar_to_cartesian(cx, cy, angle, max_radius * dist_ratio)
    size = 5 + dist_ratio * 5  # scale radius by data value
    color = "#00ccff" if dist_ratio > 0.7 else "#004466"
    svg += f'''
  <circle cx="{x:.2f}" cy="{y:.2f}" r="{size:.2f}" fill="{color}" opacity="0.8">
    <animate attributeName="r" values="{size};{size+4};{size}" dur="2s" repeatCount="indefinite" begin="{i * 0.4}s"/>
  </circle>
  <text x="{x + 10:.2f}" y="{y:.2f}" fill="#00ffcc" font-family="monospace" font-size="10">{label}</text>
'''

svg += f'''
  <text x="20" y="280" fill="#00ffcc" font-family="monospace" font-size="12">Last Update: {datetime.utcnow().isoformat()}Z</text>
</svg>
'''

with open("assets/intelligence_radar.svg", "w", encoding="utf-8") as f:
    f.write(svg)
