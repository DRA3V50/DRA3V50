from PIL import Image, ImageDraw
import subprocess, math

SIZE = 520
CENTER = SIZE // 2
RADIUS = 220
BG = (5, 15, 30)          # Dark SOC blue
RADAR = (0, 200, 255)     # Cyan
BLIP = (0, 255, 200)

# Map directories → domains
DOMAINS = {
    "soc": 0,
    "ir": 60,
    "siem": 120,
    "soar": 180,
    "edr": 240,
    "data": 300
}

def get_activity():
    result = subprocess.check_output(
        ["git", "log", "--name-only", "--pretty=format:"],
        text=True
    )

    activity = {k: 0 for k in DOMAINS}

    for line in result.splitlines():
        for domain in DOMAINS:
            if line.lower().startswith(domain + "/"):
                activity[domain] += 1

    return activity

activity = get_activity()
frames = []

for sweep in range(0, 360, 5):
    img = Image.new("RGB", (SIZE, SIZE), BG)
    d = ImageDraw.Draw(img)

    # Radar circle
    d.ellipse(
        (CENTER-RADIUS, CENTER-RADIUS, CENTER+RADIUS, CENTER+RADIUS),
        outline=RADAR, width=2
    )

    # Sweep
    angle = math.radians(sweep)
    sx = CENTER + RADIUS * math.cos(angle)
    sy = CENTER + RADIUS * math.sin(angle)
    d.line((CENTER, CENTER, sx, sy), fill=RADAR, width=2)

    # Plot activity blips
    for domain, base_angle in DOMAINS.items():
        count = activity[domain]
        for i in range(count):
            r = 40 + i * 12
            a = math.radians(base_angle)
            x = CENTER + r * math.cos(a)
            y = CENTER + r * math.sin(a)
            d.ellipse((x-3, y-3, x+3, y+3), fill=BLIP)

    frames.append(img)

frames[0].save(
    "generated.gif",
    save_all=True,
    append_images=frames[1:],
    duration=80,
    loop=0
)

