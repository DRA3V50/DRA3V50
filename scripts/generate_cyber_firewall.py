import random
from datetime import datetime

svg_template = """
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600">
  <rect width="600" height="600" fill="#0a0f1a"/>
  
  <!-- Central Firewall -->
  <circle cx="300" cy="300" r="50" fill="#ff4e4e">
    <animate attributeName="r" values="50;60;50" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <text x="270" y="305" font-family="Consolas, monospace" font-size="14" fill="#ffffff">FIREWALL</text>
  
  {beams}
</svg>
"""

beam_template = """
<line x1="{x1}" y1="{y1}" x2="300" y2="300" stroke="{color}" stroke-width="2" opacity="0.5">
  <animate attributeName="opacity" values="0.5;1;0.5" dur="{dur}s" repeatCount="indefinite" begin="{begin}s"/>
  <animate attributeName="x1" values="{x1};300;{x1}" dur="{dur}s" repeatCount="indefinite" begin="{begin}s"/>
  <animate attributeName="y1" values="{y1};300;{y1}" dur="{dur}s" repeatCount="indefinite" begin="{begin}s"/>
</line>
"""

# Example threats / MITRE tactics
tactics = [
    "Initial Access", "Execution", "Persistence",
    "Privilege Escalation", "Defense Evasion", "Credential Access",
    "Discovery", "Lateral Movement", "Exfiltration", "Impact"
]

beams_svg = ""
for i, tactic in enumerate(tactics):
    x1 = random.randint(0, 600)
    y1 = random.choice([0, 600])  # from top or bottom edge
    color = "#{:02x}{:02x}{:02x}".format(random.randint(50,255), random.randint(50,255), random.randint(50,255))
    dur = round(random.uniform(2,5), 2)
    begin = round(random.uniform(0,2), 2)
    beams_svg += beam_template.format(x1=x1, y1=y1, color=color, dur=dur, begin=begin)

# Save SVG
with open("assets/cyber_firewall_live.svg", "w") as f:
    f.write(svg_template.format(beams=beams_svg))
