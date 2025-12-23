from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from pathlib import Path

# Output path
output = Path("generated.gif")
frames = []

# Create 6 frames showing current time
for i in range(6):
    img = Image.new("RGB", (500, 200), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    text = f"Blue Team Radar\nUpdated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    draw.text((20, 60), text, fill=(56, 189, 248))

    frames.append(img)

# Save animated GIF
frames[0].save(
    output,
    save_all=True,
    append_images=frames[1:],
    duration=800,
    loop=0
)

print("Animated GIF generated")
