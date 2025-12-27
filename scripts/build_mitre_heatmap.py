from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio

Path("assets").mkdir(exist_ok=True)

# MITRE tactics & example techniques
tactics = ["Reconnaissance", "Initial Access", "Execution", "Persistence",
           "Privilege Escalation", "Defense Evasion", "Credential Access",
           "Discovery", "Lateral Movement", "Exfiltration", "Impact"]
num_tactics = len(tactics)

techniques_per_tactic = 5
width, height = 600, 200
cell_width = width // num_tactics
cell_height = height // techniques_per_tactic
frames = []
num_frames = 20

# Font
font = ImageFont.load_default()

# Animate heatmap: cells pulse sequentially
for f in range(num_frames):
    img = Image.new("RGB", (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    for i, tactic in enumerate(tactics):
        for j in range(techniques_per_tactic):
            # Calculate pulse intensity
            pulse = ((f + i + j) % num_frames) / num_frames
            red = int(200 + 55 * pulse)
            green = int(50 + 100 * (1 - pulse))
            blue = int(50 + 100 * (1 - pulse))
            color = (red, green, blue)
            
            x0 = i * cell_width + 5
            y0 = j * cell_height + 5
            x1 = (i + 1) * cell_width - 5
            y1 = (j + 1) * cell_height - 5
            
            draw.rectangle([x0, y0, x1, y1], fill=color)
    
    # Draw tactic labels
    for i, tactic in enumerate(tactics):
        x = i * cell_width + cell_width / 2
        y = height - 15
        draw.text((x, y), tactic, fill="white", font=font, anchor="ms")
    
    frames.append(img)

# Save animated GIF
gif_path = "assets/mitre_heatmap.gif"
frames[0].save(
    gif_path,
    save_all=True,
    append_images=frames[1:],
    duration=300,
    loop=0,
    optimize=True
)

print(f"MITRE Heatmap GIF generated at {gif_path}")

