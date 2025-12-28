import svgwrite
import random
from pathlib import Path

WIDTH = 800
HEIGHT = 220
BG = "#0a0f1a"
LINE = "#2f6fed"
NODE = "#9ec7ff"
PACKET = "#b7d7ff"

output = Path("assets/network_flow.svg")
output.parent.mkdir(parents=True, exist_ok=True)

dwg = svgwrite.Drawing(
    filename=str(output),
    size=(f"{WIDTH}px", f"{HEIGHT}px"),
    viewBox=f"0 0 {WIDTH} {HEIGHT}"
)

# Background
dwg.add(dwg.rect((0, 0), (WIDTH, HEIGHT), fill=BG))

# Node positions
nodes = {
    "endpoint1": (80, 60),
    "endpoint2": (80, 160),
    "server": (380, 110),
    "cloud": (680, 110),
}

# Draw nodes
for x, y in nodes.values():
    dwg.add(dwg.circle(center=(x, y), r=10, fill=NODE))

# Links
links = [
    ("endpoint1", "server"),
    ("endpoint2", "server"),
    ("server", "cloud"),
]

for a, b in links:
    x1, y1 = nodes[a]
    x2, y2 = nodes[b]

    line = dwg.add(dwg.line(
        start=(x1, y1),
        end=(x2, y2),
        stroke=LINE,
        stroke_width=2,
        opacity=0.4
    ))

    # Flow animation
    line.update({
        "stroke-dasharray": "6 6"
    })

    line.add(dwg.animate(
        attributeName="stroke-dashoffset",
        from_="0",
        to="24",
        dur=f"{random.randint(3,6)}s",
        repeatCount="indefinite"
    ))

# Packet pulses
for _ in range(6):
    a, b = random.choice(links)
    x1, y1 = nodes[a]
    x2, y2 = nodes[b]

    packet = dwg.add(dwg.circle(
        center=(x1, y1),
        r=3,
        fill=PACKET,
        opacity=0.9
    ))

    packet.add(dwg.animateMotion(
        path=f"M{x1},{y1} L{x2},{y2}",
        dur=f"{random.randint(4,7)}s",
        repeatCount="indefinite"
    ))

dwg.save()
print("Generated assets/network_flow.svg")
