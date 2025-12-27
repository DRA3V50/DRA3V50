import svgwrite
import random

ROWS = 6
COLS = 11
WIDTH = 1100
HEIGHT = 450
CELL_W = WIDTH / COLS
CELL_H = HEIGHT / ROWS

ATTACK_IDS = [
    f"T10{str(i).zfill(2)}" for i in range(ROWS * COLS)
]

dwg = svgwrite.Drawing("mitre_dashboard.svg", size=(WIDTH, HEIGHT))

dwg.add(dwg.rect(insert=(0,0), size=(WIDTH,HEIGHT),
        fill="#0b0f0c"))

title = dwg.text(
    "MITRE ATT&CK Activity Dashboard",
    insert=(WIDTH/2, 30),
    text_anchor="middle",
    fill="#7bffd1",
    font_size="22px",
    font_family="monospace"
)
dwg.add(title)

active = random.sample(range(len(ATTACK_IDS)), 12)

for idx, tid in enumerate(ATTACK_IDS):
    r = idx // COLS
    c = idx % COLS
    x = c * CELL_W + 5
    y = r * CELL_H + 50

    glow = tid in active

    rect = dwg.rect(
        insert=(x,y),
        size=(CELL_W-10,CELL_H-10),
        rx=8,
        ry=8,
        fill="rgba(20,30,20,0.9)",
        stroke="#00ffaa" if glow else "#116644",
        stroke_width=2
    )
    dwg.add(rect)

    txt = dwg.text(
        tid,
        insert=(x+20, y+30),
        fill="#d9ffe8",
        font_size="12px",
        font_family="monospace"
    )
    dwg.add(txt)

dwg.save()

