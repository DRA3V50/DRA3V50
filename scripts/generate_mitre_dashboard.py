#!/usr/bin/env python3
import svgwrite
import time

# --- CONFIG ---
WIDTH = 650
HEIGHT = 420
BAR_WIDTH = 360
BAR_HEIGHT = 14
BAR_SPACING = 34
LEFT_MARGIN = 170

TECHS = [
    ("Initial Access", 70),
    ("Execution", 85),
    ("Persistence", 65),
    ("Privilege Escalation", 75),
    ("Defense Evasion", 90),
    ("Credential Access", 80),
    ("Discovery", 88),
    ("Collection", 72),
]

BLUE = "#00e6ff"
CYAN = "#7fffd4"
GRAY = "#1d1f21"
GREEN = "#42f57b"
TEXT = "#e6e6e6"

dwg = svgwrite.Drawing(
    "mitre_dashboard.svg",
    size=(f"{WIDTH}px", f"{HEIGHT}px"),
    profile='tiny'
)

# BACKGROUND
dwg.add(dwg.rect(insert=(0,0), size=("100%","100%"), fill="#0a0f12"))

# HEADER
dwg.add(dwg.text(
    "DEFENSIVE COVERAGE — MITRE ATT&CK",
    insert=(20,40),
    fill=BLUE,
    font_size="20px",
    font_family="Consolas"
))

dwg.add(dwg.text(
    "Live SOC Simulation Dashboard",
    insert=(20,68),
    fill=CYAN,
    font_size="13px",
    font_family="Consolas"
))

dwg.add(dwg.text(
    f"Last Update: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}",
    insert=(20,95),
    fill="#9fa6ad",
    font_size="11px",
    font_family="Consolas"
))


# BARS
for i,(tech,percent) in enumerate(TECHS):
    y = 130 + i*BAR_SPACING

    # label
    dwg.add(dwg.text(
        tech,
        insert=(20,y+11),
        fill=TEXT,
        font_size="12px",
        font_family="Consolas"
    ))

    # background line
    dwg.add(dwg.rect(
        insert=(LEFT_MARGIN, y),
        size=(BAR_WIDTH, BAR_HEIGHT),
        rx=6,
        ry=6,
        fill=GRAY
    ))

    # coverage bar
    width_fill = BAR_WIDTH * (percent/100)
    dwg.add(dwg.rect(
        insert=(LEFT_MARGIN, y),
        size=(width_fill, BAR_HEIGHT),
        rx=6,
        ry=6,
        fill=GREEN
    ))

    # % text
    dwg.add(dwg.text(
        f"{percent}%",
        insert=(LEFT_MARGIN + BAR_WIDTH + 14, y+11),
        fill=GREEN,
        font_size="12px",
        font_family="Consolas"
    ))

    # ACTIVITY DOT
    dot = dwg.circle(center=(LEFT_MARGIN, y+7), r=4, fill=BLUE)
    dwg.add(dot)

    dot.add(dwg.animateMotion(
        path=f"M0,0 L{width_fill},0",
        dur=f"{2 + i*0.4}s",
        repeatCount="indefinite"
    ))


# FOOTER
dwg.add(dwg.text(
    "Monitoring: SIEM • EDR • IR • SOAR • Log Analytics",
    insert=(20, HEIGHT-22),
    fill="#7aa2c7",
    font_size="11px",
    font_family="Consolas"
))

dwg.save()
