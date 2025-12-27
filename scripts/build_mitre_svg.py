# scripts/build_mitre_svg.py
from pathlib import Path

# ensure assets folder exists
Path("assets").mkdir(exist_ok=True)

# example content
svg_content = """
<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="600" fill="white"/>
  <text x="50%" y="50%" font-size="40" text-anchor="middle" fill="black">
    MITRE Coverage
  </text>
</svg>
"""

with open("assets/mitre.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("MITRE SVG generated at assets/mitre.svg")

