from pathlib import Path
import random
import cairosvg
import imageio
from PIL import Image
import io

Path("assets").mkdir(exist_ok=True)

threats = ["Phishing", "Malware", "Lateral Movement", "Exploits", "Ransomware", "C2"]
systems = ["Endpoints", "Network", "Cloud", "Identity", "Apps", "Databases"]

cell_size = 60  # smaller for cleaner GIF
padding = 10
width = cell_size * len(threats) + padding*2
height = cell_size * len(systems) + padding*2

frames = []
num_frames = 10
target_width = 400  # resize for GitHub README
scale_ratio = target_width / width
target_height = int(height * scale_ratio)

for f in range(num_frames):
    svg_content = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        .text {{ font: bold 10px sans-serif; fill: #222; }}
        .cell {{ stroke: #444; stroke-width: 1.5; }}
    </style>
    '''

    # Draw cells with random alert intensity
    for row_idx, system in enumerate(systems):
        for col_idx, threat in enumerate(threats):
            x = padding + col_idx*cell_size
            y = padding + row_idx*cell_size
            intensity = random.randint(100, 255)
            fill_color = f'rgb({intensity}, 50, 50)'
            svg_content += f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{fill_color}" class="cell"/>\n'

    # Column labels
    for col_idx, threat in enumerate(threats):
        x = padding + col_idx*cell_size + cell_size/2
        y = padding - 2
        svg_content += f'<text x="{x}" y="{y}" class="text" text-anchor="middle">{threat}</text>\n'

    # Row labels
    for row_idx, system in enumerate(systems):
        x = padding - 2
        y = padding + row_idx*cell_size + cell_size/2 + 4
        svg_content += f'<text x="{x}" y="{y}" class="text" text-anchor="end">{system}</text>\n'

    svg_content += "</svg>"

    # Convert SVG to PNG bytes
    png_data = cairosvg.svg2png(bytestring=svg_content.encode("utf-8"))
    image = Image.open(io.BytesIO(png_data))
    
    # Resize for clean README display
    image = image.resize((target_width, target_height), Image.ANTIALIAS)
    frames.append(image)

# Save GIF
gif_path = "assets/threat_matrix.gif"
frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=500, loop=0, optimize=True)

print(f"Animated Threat Matrix GIF generated at {gif_path}")
