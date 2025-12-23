from PIL import Image, ImageDraw
import json, math, random

SIZE = 520
CENTER = SIZE // 2
RADIUS = 220

SEVERITY_COLORS = {
    "critical": "red",
    "high": "orange",
    "medium": "yellow",
    "low": "lime"
}

LABELS = [
    ("🛡️ SOC", 270),
    ("🚨 IR", 330),
    ("📊 SIEM", 30),
    ("⚙️ SOAR", 90),
    ("🧬 EDR", 150),
    ("📈 DATA", 210)
]

with open("metrics.json") as f:
    metrics = list(json.items(json.load(f)))

frames = []

for sweep in range(0, 360, 6):
    img = Image.new("RGB", (SIZE, SIZE), "black")
    d = ImageDraw.Draw(img)

    # Outer radar circle
    d.ellipse(
        (CENTER-RADIUS, CENTER-RADIUS, CENTER+RADIUS, CENTER+RADIUS),
        outline="green", width=3
    )

    # Sector lines (6)
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        x = CENTER + RADIUS * math.cos(rad)
        y = CENTER + RADIUS * math.sin(rad)
        d.line((CENTER, CENTER, x, y), fill="green")

    # Labels
    for text, angle in LABELS:
        rad = math.radians(angle)
        x = CENTER + (RADIUS + 10) * math.cos(rad)
        y = CENTER + (RADIUS + 10) * math.sin(rad)
        d.text((x-20, y-10), text, fill="white")

    # Radar sweep
    rad = math.radians(sweep)
    sx = CENTER + RADIUS * math.cos(rad)
    sy = CENTER + RADIUS * math.sin(rad)
    d.line((CENTER, CENTER, sx, sy), fill="lime", width=2)

    # Blips
    for i, (domain, data) in enumerate(metrics):
        start_angle = i * 60
        end_angle = start_angle + 60

        for _ in range(data["count"]):
            a = math.radians(random.uniform(start_angle, end_angle))
            r = random.randint(20, RADIUS-15)
            bx = CENTER + r * math.cos(a)
            by = CENTER + r * math.sin(a)

            d.ellipse(
                (bx-3, by-3, bx+3, by+3),
                fill=SEVERITY_COLORS[data["severity"]]
            )

    frames.append(img)

frames[0].save(
    "generated.gif",
    save_all=True,
    append_images=frames[1:],
    duration=110,
    loop=0
)

