from pathlib import Path
import random
import cairosvg
import imageio

Path("assets").mkdir(exist_ok=True)

# Threat matrix
threats = ["Phishing", "Malware", "Lateral Movement", "Exploits", "Ransomware", "C2"]
systems = ["Endpoints", "Network", "Cloud", "Identity", "Apps", "Databases"]

cell_size = 80
padding = 20
width = cell_size * len(threats) + padding*2
height = cell_size * len(systems) + padding*2

frames = []

# Generate multiple frames for animation
num_frames = 10

for f in range(num_frames):
    svg_content = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        .text {{ font: bold 12px sans-serif; fill: #222; }}
        .cell {{ stroke: #444; stroke-width: 2; }}
    </style>
    '''
    
    # Draw cells with random “alert intensity”
    for row_idx, system in enumerate(systems):
        for col_idx, threat in enumerate(threats):
            x = padding + col_idx*cell_size
            y = padding + row_idx*cell_size
            # Random alert intensity per frame
            intensity = random.randint(100, 255)
            fill_color = f'rgb({intensity}, 50, 50)'
            svg_content += f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{fill_color}" class="cell"/>\n'
    
    # Column labels
    for col_idx, threat in enumerate(threats):
        x = padding + col_idx*cell_size + cell_size/2
        y = padding - 5
        svg_content += f'<text x="{x}" y="{y}" class="text" text-anchor="middle">{threat}</text>\n'

    # Row labels
    for row_idx, system in enumerate(systems):
        x = padding - 5
        y = padding + row_idx*cell_size + cell_size/2 + 4
        svg_content += f'<text x="{x}" y="{y}" class="text" text-anchor="end">{system}</text>\n'

    svg_content += "</svg>"

    # Convert SVG to PNG bytes
    png_data = cairosvg.svg2png(bytestring=svg_content.encode("utf-8"))
    frames.append(imageio.imread(png_data))

# Save GIF
gif_path = "assets/threat_matrix.gif"
imageio.mimsave(gif_path, frames, duration=0.5)  # 0.5s per frame

print(f"Animated Threat Matrix GIF generated at {gif_path}")
