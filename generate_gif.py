from PIL import Image, ImageDraw
import json
import random

with open("metrics.json") as f:
    m = json.load(f)

frames = []

for _ in range(15):
    img = Image.new("RGB", (400, 400), "black")
    d = ImageDraw.Draw(img)

    # Radar circle
    d.ellipse((50, 50, 350, 350), outline="green", width=3)

    # Alert blips
    for _ in range(m["alerts"]):
        x = random.randint(70, 330)
        y = random.randint(70, 330)
        d.ellipse((x-4, y-4, x+4, y+4), fill="red")

    # Metrics text
    d.text((10, 10), f"Alerts: {m['alerts']}", fill="white")
    d.text((10, 30), f"Incidents: {m['incidents']}", fill="white")
    d.text((10, 50), f"Automation: {m['automation']}", fill="white")
    d.text((10, 70), f"Audits: {m['audits']}", fill="white")

    frames.append(img)

frames[0].save(
    "generated.gif",
    save_all=True,
    append_images=frames[1:],
    duration=200,
    loop=0
)
