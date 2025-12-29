import random
from pathlib import Path

WIDTH, HEIGHT = 600, 400
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

output = Path("assets/cyber_pulse.svg")
output.parent.mkdir(parents=True, exist_ok=True)

# Example MITRE-aligned / analyst-relevant lines (label, amplitude, speed)
data_lines = [
    ("Initial Access", 40, 6),
    ("Execution", 30, 5.5),
    ("Persistence", 25, 7),
    ("Privilege Escalation", 35, 6.5),
    ("Defense Evasion", 28, 5),
    ("Credential Access", 32, 6.2),
    ("Discovery", 22, 4.8),
    ("Lateral Movement", 30, 5.7),
    ("Exfiltration", 38, 6.8),
    ("Impact", 40, 7.2),
]

# SVG header
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <rect width="{WIDTH}" height="{HEIGHT}" fill="#0a0f1a"/>
  <defs>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#4effff" flood-opacity="0.8"/>
    </filter>
    <linearGradient id="lineGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2f6fed"/>
      <stop offset="100%" stop-color="#5cb3ff"/>
    </linearGradient>
  </defs>
'''

# Draw baseline grid lines
for y in range(50, HEIGHT, 50):
    svg += f'<line x1="0" y1="{y}" x2="{WIDTH}" y2="{y}" stroke="#1e2a45" stroke-width="1"/>\n'

# Draw animated waveform lines
for i, (label, amplitude, speed) in enumerate(data_lines):
    y_base = 50 + i * 30  # vertical spacing
    dur = round(random.uniform(4.5, 6.5), 2)
    begin = round(random.uniform(0, 3), 2)

    # Draw the animated line using path and animateTransform for simple pulse
    svg += f'''
  <path d="M0,{y_base}" fill="none" stroke="url(#lineGrad)" stroke-width="3" filter="url(#glow)">
    <animate attributeName="d"
      dur="{dur}s" repeatCount="indefinite"
      values="
        M0,{y_base} 
        {' '.join(f'L{j},{y_base + random.randint(-amplitude, amplitude)}' for j in range(50, WIDTH+50, 50))};
        M0,{y_base} 
        {' '.join(f'L{j},{y_base + random.randint(-amplitude, amplitude)}' for j in range(50, WIDTH+50, 50))};
      "
      begin="{begin}s"/>
  </path>
  <text x="10" y="{y_base - 5}" font-family="Consolas, monospace" font-size="12" fill="#a0c8ff">{label}</text>
'''

svg += '</svg>'

with open(output, "w") as f:
    f.write(svg)

print(f"Cyber Pulse SVG saved to {output}")

