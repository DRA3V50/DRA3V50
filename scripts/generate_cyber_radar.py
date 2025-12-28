import svgwrite
import random
from math import cos, sin, radians
from pathlib import Path

WIDTH, HEIGHT = 400, 400
CENTER = (WIDTH // 2, HEIGHT // 2)
RADAR_RADIUS = 180

output = Path("assets/cyber_radar.svg")
output.parent.mkdir(parents=True, exist_ok=True)

dwg = svgwrite.Drawing(
    filename=str(output),
    size=(f"{WIDTH}px", f"{HEIGHT}px"),
    viewBox=f"0 0 {WIDTH} {HEIGHT}",
)

# Background
dwg.add(dwg.rect(insert=(0, 0), size=(WIDTH, HEIGHT), fill="#0a0f1a"))

# Radar circles
for r in range(40, RADAR_RADIUS + 1, 40):
    dwg.add(dwg.circle(center=CENTER, r=r, fill="none", stroke="#2f6fed", stroke_width=1, opacity=0.3))

# Radar lines
for angle in range(0, 360, 45):
    rad = radians(angle)
    x = CENTER[0] + RADAR_RADIUS * cos(rad)
    y = CENTER[1] + RADAR_RADIUS * sin(rad)
    dwg.add(dwg.line(start=CENTER, end=(x, y), stroke="#2f6fed", stroke_width=1, opacity=0.3))

# Rotating sweep (pie slice with gradient)
sweep_gradient = dwg.linearGradient(id="sweepGradient", gradientTransform="rotate(45)")
sweep_gradient.add_stop_color(offset='0%', color="#2f6fed")
sweep_gradient.add_stop_color(offset='100%', color="#2f6fed", opacity=0)
dwg.defs.add(sweep_gradient)

sweep = dwg.path(
    d=f"M{CENTER[0]},{CENTER[1]} L{CENTER[0]+RADAR_RADIUS},{CENTER[1]} A{RADAR_RADIUS},{RADAR_RADIUS} 0 0,1 {CENTER[0]+int(RADAR_RADIUS*0.7)},{CENTER[1]-int(RADAR_RADIUS*0.7)} Z",
    fill="url(#sweepGradient)",
    opacity=0.25,
)
dwg.add(sweep)

# Correctly attach animation to the sweep
sweep_anim = dwg.animateTransform(
    attributeName="transform",
    type="rotate",
    from_="0 200 200",
    to="360 200 200",
    dur="6s",
    repeatCount="indefinite"
)
sweep.add(sweep_anim)

# Pulsing threat blips
for i in range(10):
    angle = random.uniform(0, 360)
    distance = random.uniform(20, RADAR_RADIUS)
    rad = radians(angle)
    x = CENTER[0] + distance * cos(rad)
    y = CENTER[1] + distance * sin(rad)

    circle = dwg.circle(center=(x, y), r=6, fill="#5cb3ff", opacity=0.6)
    dwg.add(circle)
    
    # Animate radius
    anim = dwg.animate(
        attributeName="r",
        values="6;10;6",
        dur=f"{random.uniform(2,4):.2f}s",
        repeatCount="indefinite",
        begin=f"{random.uniform(0,4):.2f}s"
    )
    circle.add(anim)

    # Animate opacity
    opacity_anim = dwg.animate(
        attributeName="opacity",
        values="0.6;1;0.6",
        dur=f"{random.uniform(2,4):.2f}s",
        repeatCount="indefinite",
        begin=f"{random.uniform(0,4):.2f}s"
    )
    circle.add(opacity_anim)

dwg.save()
print("Generated assets/cyber_radar.svg")
