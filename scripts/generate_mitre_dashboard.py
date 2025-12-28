import svgwrite

WIDTH = 680
HEIGHT = 300
BAR_WIDTH = 390
BAR_HEIGHT = 10
X_OFFSET = 210
Y_OFFSET = 85
SPACING = 40

BLUE = "#00c8ff"
BG = "#0a0f1a"
TEXT = "#e8f1ff"

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
)

# background
dwg.add(dwg.rect((0, 0), (WIDTH, HEIGHT), fill=BG))

# title
dwg.add(dwg.text(
    "Operational Defense Coverage",
    insert=(28, 40),
    fill=TEXT,
    font_size="20px",
    font_family="Segoe UI"
))

# subtitle
dwg.add(dwg.text(
    "Blue Team Defense Operations • Analyst Dashboard",
    insert=(28, 60),
    fill="#7ea6ff",
    font_size="12px"
))


for i, (label, percent) in enumerate(coverage):
    y = Y_OFFSET + i * SPACING

    # label
    dwg.add(dwg.text(
        label,
        insert=(28, y + 8),
        fill=TEXT,
        font_size="13px"
    ))

    # base bar
    dwg.add(dwg.rect(
        (X_OFFSET, y),
        (BAR_WIDTH, BAR_HEIGHT),
        fill="#0e2238",
        rx=5, ry=5
    ))

    # filled portion
    bar = dwg.rect(
        (X_OFFSET, y),
        (BAR_WIDTH * percent / 100, BAR_HEIGHT),
        fill=BLUE,
        rx=5, ry=5
    )
    bar.attribs["opacity"] = 0.9
    dwg.add(bar)

    # animated activity dot
    dot = dwg.circle(
        center=(X_OFFSET + 6, y + BAR_HEIGHT/2),
        r=3.5,
        fill="#baf2ff"
    )

    dot.add(dwg.animateMotion(
        path=f"M0,0 L{BAR_WIDTH * percent / 100 - 12},0",
        dur=f"{2 + i*0.35}s",
        repeatCount="indefinite"
    ))

    dwg.add(dot)

    # percentage
    dwg.add(dwg.text(
        f"{percent}%",
        insert=(X_OFFSET + BAR_WIDTH + 14, y + 9),
        fill="#9ccaff",
        font_size="12px"
    ))

dwg.save()

