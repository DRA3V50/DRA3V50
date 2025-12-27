from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio

Path("assets").mkdir(exist_ok=True)

# MITRE tactics and example coverage percentages
tactics = ["Recon", "Initial Access", "Execution", "Persistence",
           "Privilege Escalation", "Defense Evasion", "Credential Access",
           "Discovery", "Lateral Movement", "Exfiltration", "Impact"]
coverage = [0.8, 0.6, 0.7, 0.5, 0.6, 0.9, 0.4, 0.7, 0.5, 0.6, 0.3]  # 0.0 to 1.0

# Adjusted layout
width, height = 700, 500  # taller canvas
bar_height = 30            # thicker bars
bar_spacing = 15           # more spacing between bars
frames = []
num_frames = 30

# Font
font = ImageFont.load_default()

for f in range(num_frames):
    img = Image.new("RGB", (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    for i, tactic in enumerate(tactics):
        y0 = i*(bar_height + bar_spacing) + 40
        y1 = y0 + bar_height
        x0 = 200
        x1 = x0 + int(coverage[i]*400*(f/num_frames))  # animate fill

        # Bar background
        draw.rectangle([x0, y0, x0 + 400, y1], fill=(50,50,50))
        # Animated fill
        draw.rectangle([x0, y0, x1, y1], fill=(0, 120, 255))

        # Tactic label
        draw.text((10, y0 + bar_height//4), tactic, fill="white", font=font)

        # Percentage label
        perc = int(coverage[i]*100*(f/num_frames))
        draw.text((x0 + 410, y0 + bar_height//4), f"{perc}%", fill="white", font=font)

    frames.append(img)

# Save GIF
gif_path = "assets/mitre_bar_chart.gif"
frames[0].save(
    gif_path,
    save_all=True,
    append_images=frames[1:],
    duration=200,
    loop=0,
    optimize=True
)

print(f"MITRE Bar Chart GIF generated at {gif_path}")

