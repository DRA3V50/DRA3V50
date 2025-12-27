from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio

Path("assets").mkdir(exist_ok=True)

# SOC-relevant MITRE tactics only
tactics = ["Reconnaissance", "Initial Access", "Persistence",
           "Privilege Escalation", "Defense Evasion", "Credential Access",
           "Lateral Movement", "Exfiltration", "Impact"]
coverage = [0.8, 0.6, 0.5, 0.6, 0.9, 0.4, 0.5, 0.6, 0.3]  # 0.0 to 1.0

# Layout for side-by-side display
width, height = 500, 500  # taller for spacing
bar_height = 40            # bigger bars for readability
bar_spacing = 25           # generous spacing
frames = []
num_frames = 30

# Font
font = ImageFont.load_default()

for f in range(num_frames):
    img = Image.new("RGB", (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    for i, tactic in enumerate(tactics):
        y0 = i*(bar_height + bar_spacing) + 30
        y1 = y0 + bar_height
        x0 = 180
        x1 = x0 + int(coverage[i]*250*(f/num_frames))  # animate fill, shorter width for side-by-side

        # Bar background
        draw.rectangle([x0, y0, x0 + 250, y1], fill=(50,50,50))
        # Animated fill
        draw.rectangle([x0, y0, x1, y1], fill=(0, 120, 255))

        # Tactic label (SOC-relevant)
        draw.text((10, y0 + bar_height//4), tactic, fill="white", font=font)

        # Percentage label
        perc = int(coverage[i]*100*(f/num_frames))
        draw.text((x0 + 260, y0 + bar_height//4), f"{perc}%", fill="white", font=font)

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
