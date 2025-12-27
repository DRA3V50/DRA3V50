import json

WIDTH = 420
BAR_HEIGHT = 14
BAR_GAP = 10
START_X = 160
MAX_BAR = 220
START_Y = 40

with open("mitre-coverage.json") as f:
    data = json.load(f)

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{WIDTH}" height="260" viewBox="0 0 {WIDTH} 260" '
    f'role="img" aria-label="MITRE ATT&CK Coverage">',
    '<rect x="0" y="0" width="100%" height="100%" fill="#0d1117"/>'
]

y = START_Y
delay = 0

for tactic, value in data.items():
    bar_width = int(MAX_BAR * value)

    svg.append(f'''
    <text x="10" y="{y+11}" fill="#c9d1d9" font-size="11">{tactic}</text>

    <rect x="{START_X}" y="{y}" width="{bar_width}" height="{BAR_HEIGHT}"
          fill="rgba(88,166,255,0.85)">
      <animate attributeName="opacity"
               values="0.6;1;0.6"
               dur="8s"
               begin="{delay}s"
               repeatCount="indefinite"/>
    </rect>
    ''')

    y += BAR_HEIGHT + BAR_GAP
    delay += 0.6

svg.append("</svg>")

with open("assets/mitre.svg", "w") as f:
    f.write("\n".join(svg))
