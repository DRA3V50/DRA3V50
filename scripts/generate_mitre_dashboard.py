import svgwrite
import random

WIDTH = 680
HEIGHT = 360
BAR_WIDTH = 420
BAR_HEIGHT = 12
X_OFFSET = 180
Y_OFFSET = 90
SPACING = 44

blue = "#00c8ff"
bg = "#0a0f1a"
grid = "#102235"
text = "#e8f1ff"

coverage = [
    ("Threat Detection Engineering", 78),
    ("Endpoint Telemetry Analysis", 92),
    ("SIEM Hunting & Correlation", 84),
    ("Incident Response Readiness", 71),
    ("Threat Intel Mapping", 66),
]

dwg = svgwrite.Drawing(
    "mitre_dashboard.svg",
    size=(f"{WIDTH}px", f"{HEIGHT}px"),
    debug=False
)

# background
dwg.add(dwg.rect((0, 0), (WIDTH, HEIGHT), fill=bg))


# title
dwg.add(dwg.text(
    "Operational Defense Coverage",
    insert=(30, 46),
    fill=text,
    font_size="22px",
    font_family="Segoe UI",
))

# subtle subtitle
dwg.add(dwg.text(
    "Blue Team Defense Operations • Analyst Dashboard",
    insert=(30, 72),
    fill="#7ea6ff",
    font_size="13px",
))


for i, (label, percent) in enumerate(coverage):
    y = Y_OFFSET + i * SPACING

    # label
    dwg.add(dwg.text(
        label,
        insert=(30, y + 10),
        fill=text,
        font_size="14px",
    ))

    # base line
    dwg.add(dwg.rect(
        (X_OFFSET, y),
        (BAR_WIDTH, BAR_HEIGHT),
        fill="#0e2238",
        rx=5, ry=5
    ))

    # coverage bar
    fill = dwg.rect(
        (X_OFFSET, y),
        (BAR_WIDTH * percent / 100, BAR_HEIGHT),
        fill=blue,
        rx=5, ry=5
    )
    fill.attribs["opacity"] = 0.9
    dwg.add(fill)

    # activity dot
    dot = dwg.circle(
        center=(X_OFFSET + 6, y + BAR_HEIGHT/2),
        r=4,
        fill="#9be9ff"
    )

    # animated motion
    dot.add(dwg.animateMotion(
        path=f"M0,0 L{BAR_WIDTH * percent / 100 - 12},0",
        dur=f"{2 + i*0.4}s",
        repeatCount="indefinite"
    ))

    dwg.add(dot)

    # % text
    dwg.add(dwg.text(
        f"{percent}%",
        insert=(X_OFFSET + BAR_WIDTH + 16, y + 11),
        fill="#99c6ff",
        font_size="13px",
    ))


dwg.save()
