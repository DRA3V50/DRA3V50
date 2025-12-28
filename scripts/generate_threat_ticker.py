import svgwrite
from pathlib import Path

WIDTH = 420
HEIGHT = 60
BG = "#0a0f1a"

items = [
    "Suspicious Lateral Movement",
    "Anomalous EDR Activity",
    "Beaconing Behavior Detected",
    "Authentication Risk Spike",
]

# Ensure assets directory exists
output_path = Path("assets/threat_ticker.svg")
output_path.parent.mkdir(parents=True, exist_ok=True)

dwg = svgwrite.Drawing(
    filename=str(output_path),
    size=(f"{WIDTH}px", f"{HEIGHT}px")
)

dwg.add(dwg.rect((0, 0), (WIDTH, HEIGHT), fill=BG))

dwg.add(dwg.text(
    "Threat Intel Stream",
    insert=(16, 22),
    font_size="13px",
    fill="#9ec7ff"
))

group = dwg.g(font_size="12px", fill="#d9e9ff")

x = WIDTH
for item in items:
    text = group.add(dwg.text(item, insert=(x, 44)))
    text.add(dwg.animate(
        attributeName="x",
        from_=str(WIDTH),
        to="-300",
        dur="14s",
        repeatCount="indefinite"
    ))
    x += 220

dwg.add(group)
dwg.save()

print("SVG written to assets/threat_ticker.svg")
