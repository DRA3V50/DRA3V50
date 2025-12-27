from PIL import Image, ImageDraw
import math
import datetime
import os

size = 500
frames = 40
radius = size // 2

os.makedirs("assets", exist_ok=True)

images = []
for f in range(frames):
    img = Image.new("RGBA", (size, size), (5, 10, 20, 255))
    draw = ImageDraw.Draw(img)

    # radar circle
    draw.ellipse((20,20,size-20,size-20), outline=(0,255,0), width=2)

    # sweeping line
    angle = (f / frames) * 2 * math.pi
    x = radius + radius * math.cos(angle)
    y = radius + radius * math.sin(angle)

    draw.line((radius, radius, x, y), fill=(0,255,0), width=3)

    # dots (fake activity)
    for i in range(8):
        dx = radius + math.cos(i) * (radius-40)
        dy = radius + math.sin(i) * (radius-40)
        draw.ellipse((dx-4,dy-4,dx+4,dy+4), fill=(0,255,0))

    draw.text((10,size-30), f"Updated: {datetime.datetime.utcnow()} UTC", fill=(0,255,0))

    images.append(img)

images[0].save(
    "assets/radar.gif",
    save_all=True,
    append_images=images[1:],
    optimize=False,
    duration=80,
    loop=0
)
