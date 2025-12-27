import svgwrite
import json
import time

# Load MITRE coverage
with open('coverage.json') as f:
    coverage = json.load(f)

svg_height = 100 + len(coverage) * 30
dwg = svgwrite.Drawing('mitre_dashboard.svg', size=("700px", f"{svg_height}px"))

# Background
dwg.add(dwg.rect((0, 0), ("700px", f"{svg_height}px"), fill="#0a0f14"))

# Add timestamp comment correctly
dwg.add(svgwrite.base.Comment(f"Updated: {time.time()}"))

# Title
dwg.add(dwg.text("MITRE ATT&CK Coverage (Blue Team)", insert=(20, 40),
                 fill="#00d8ff", font_size="22px", font_weight="bold"))

# Glow filter
filter_glow = dwg.defs.add(dwg.filter(id="glow"))
filter_glow.feGaussianBlur(in_="SourceGraphic", stdDeviation=2, result="blur")
filter_glow.feMerge(layernames=["blur", "SourceGraphic"])

# Bars
x_start = 20
y_start = 70
bar_width = 250
bar_height = 15
bar_spacing = 30

for i, (tactic, percent) in enumerate(coverage.items()):
    # Label
    dwg.add(dwg.text(tactic, insert=(x_start, y_start + i*bar_spacing + 12),
                     fill="#a0e0ff", font_size="14px"))
    # Background bar
    dwg.add(dwg.rect(insert=(x_start + 160, y_start + i*bar_spacing),
                     size=(bar_width, bar_height), fill="#1a2a3a", rx=3, ry=3))
    # Coverage bar with animation
    bar = dwg.rect(insert=(x_start + 160, y_start + i*bar_spacing),
                   size=(bar_width * percent / 100, bar_height),
                   fill="#00d8ff", rx=3, ry=3)
    dwg.add(bar)
    bar.add(dwg.animate(attributeName="fill",
                        values="#00d8ff;#80f0ff;#00d8ff",
                        dur=f"{1.5 + i*0.2}s",
                        repeatCount="indefinite"))

dwg.save()
