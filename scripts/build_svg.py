import json
import math

CENTER = 200
MIN_R = 45
MAX_R = 120

with open("radar-values.json") as f:
    values = json.load(f)

points = []
n = len(values)

for i, v in enumerate(values):
    angle = (2 * math.pi / n) * i - math.pi / 2
    r = MIN_R + v * (MAX_R - MIN_R)
    x = CENTER + r * math.cos(angle)
    y = CENTER + r * math.sin(angle)
    points.append(f"{round(x,1)},{round(y,1)}")

with open("assets/radar.svg") as f:
    svg = f.read()

svg = svg.replace("{{POINTS}}", " ".join(points))

with open("assets/radar.svg", "w") as f:
    f.write(svg)

