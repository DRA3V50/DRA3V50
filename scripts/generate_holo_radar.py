# scripts/generate_holo_radar.py
import math
import random

SVG_FILE = "assets/cyber_radar_holo.svg"
WIDTH, HEIGHT = 600, 600
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
RADIUS = 200

# Nodes to display (example SOC hosts)
nodes = [
    {"name": "Workstation1", "angle": 0},
    {"name": "Server1", "angle": 60},
    {"name": "DBServer", "angle": 120},
    {"name": "Firewall", "angle": 180},
    {"name": "Router", "angle": 240},
    {"name": "SensorX", "angle": 300}
]

def polar_to_cartesian(angle_deg, r):
    angle_rad = math.radians(angle_deg)
    x = CENTER_X + r * math.cos(angle_rad)
    y = CENTER_Y + r * math.sin(angle_rad)
    return x, y

def random_pulse_duration():
    return round(random.uniform(2, 5), 2)

def generate_svg():
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">\n'
    svg += f'  <rect width="{WIDTH}" height="{HEIGHT}" fill="#0a0f1a"/>\n'
    svg += '  <defs>\n'
    svg += '    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">\n'
    svg += '      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#4effff" flood-opacity="0.8"/>\n'
    svg += '    </filter>\n'
    svg += '    <radialGradient id="sweepGrad" cx="50%" cy="50%" r="50%">\n'
    svg += '      <stop offset="0%" stop-color="#2f6fed" stop-opacity="0.3"/>\n'
    svg += '      <stop offset="100%" stop-color="#2f6fed" stop-opacity="0"/>\n'
    svg += '    </radialGradient>\n'
    svg += '  </defs>\n'

    # Draw outer orbit rings for MITRE ATT&CK coverage
    for r in range(50, RADIUS+1, 50):
        svg += f'  <circle cx="{CENTER_X}" cy="{CENTER_Y}" r="{r}" fill="none" stroke="#2f6fed" stroke-width="1" opacity="0.3"/>\n'

    # Sweep line
    svg += f'  <path d="M{CENTER_X},{CENTER_Y} L{CENTER_X+RADIUS},{CENTER_Y}" fill="url(#sweepGrad)" filter="url(#glow)">\n'
    svg += f'    <animateTransform attributeName="transform" attributeType="XML" type="rotate" from="0 {CENTER_X} {CENTER_Y}" to="360 {CENTER_X} {CENTER_Y}" dur="10s" repeatCount="indefinite"/>\n'
    svg += '  </path>\n'

    # Draw nodes
    for node in nodes:
        x, y = polar_to_cartesian(node["angle"], RADIUS)
        pulse_dur = random_pulse_duration()
        svg += f'  <circle cx="{x}" cy="{y}" r="6" fill="#4effff" filter="url(#glow)" opacity="0.8">\n'
        svg += f'    <animate attributeName="r" values="6;12;6" dur="{pulse_dur}s" repeatCount="indefinite"/>\n'
        svg += f'    <animate attributeName="opacity" values="0.6;1;0.6" dur="{pulse_dur}s" repeatCount="indefinite"/>\n'
        svg += f'    <title>{node["name"]}</title>\n'
        svg += '  </circle>\n'
        svg += f'  <text x="{x+8}" y="{y+4}" font-family="Consolas, monospace" font-size="12" fill="#a0c8ff">{node["name"]}</text>\n'

    svg += '</svg>'
    with open(SVG_FILE, "w") as f:
        f.write(svg)
    print(f"SVG generated: {SVG_FILE}")

if __name__ == "__main__":
    generate_svg()

