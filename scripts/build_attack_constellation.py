from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio
import random

Path("assets").mkdir(exist_ok=True)

# Skills / tools
nodes = [
    "Splunk", "Python", "SOAR", "Azure Sentinel", "CrowdStrike",
    "Nessus", "PowerShell", "Threat Intel", "Windows", "Linux"
]

# Node positions (randomly within canvas)
width, height = 500, 400
node_positions = {node: (random.randint(50, width-50), random.randint(50, height-50)) for node in nodes}

# Connections (simplified workflow)
edges = [
    ("Splunk", "SOAR"), ("Python", "SOAR"), ("Azure Sentinel", "SOAR"),
    ("CrowdStrike", "Threat Intel"), ("Nessus", "Python"),
    ("Windows", "Splunk"), ("Linux", "Splunk")
]

# Animation settings
frames = []
num_frames = 20
node_radius = 20
font = ImageFont.load_default()

for f in range(num_frames):
    img = Image.new("RGB", (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Draw edges
    for n1, n2 in edges:
        x1, y1 = node_positions[n1]
        x2, y2 = node_positions[n2]
        # Optional: animate edge brightness
        intensity = 100 + (f*10 % 155)
        color = (intensity, intensity, intensity)
        draw.line([x1, y1, x2, y2], fill=color, width=2)

    # Draw nodes
    for node, (x, y) in node_positions.items():
        # Pulse animation
        pulse = 1 + 0.2 * (f % 5)
        r = int(node_radius * pulse)
        color = (0, 120 + f*5 % 135, 255)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color, outline=(255,255,255))
        w, h = draw.textsize(node, font=font)
        draw.text((x-w/2, y-h/2), node, fill="white", font=font)

    frames.append(img)

# Save GIF
gif_path = "assets/attack_constellation.gif"
frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=200, loop=0, optimize=True)

print(f"Attack Constellation GIF generated at {gif_path}")
