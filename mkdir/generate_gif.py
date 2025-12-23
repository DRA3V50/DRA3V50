from PIL import Image, ImageDraw, ImageFont
import json
import numpy as np

# Load metrics
with open("metrics.json") as f:
    data = json.load(f)

alerts = data["alerts"]
incidents = data["incidents"]
automation = data["automation"]
audits = data["audits"]

frames = []

for t in range(20):
    img = Image.new("RGB", (400, 400), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw radar circle
    draw.ellipse([50, 50, 350, 350], outline="green", width=3)

    # Draw random alert blips
    for _ in range(alerts):
        x = np.random.randint(60, 340)
        y = np.random.randint(60, 340)
        draw.ellipse([x-5, y-5, x+5, y+5], fill="red")

    # Overlay text metrics
    draw.text((10, 10), f"Alerts Triaged: {alerts}", fill="white")
    draw.text((10, 30), f"Incidents Escalated: {incidents}", fill="white")
    draw.text((10, 50), f"Automations Run: {automation}", fill="white")
    draw.text((10, 70), f"Audits Completed: {audits}", fill="white")

    frames.append(img)

# Save as animated GIF
frames[0].save("generated.gif", save_all=True, append_images=frames[1:], duration=200, loop=0)
