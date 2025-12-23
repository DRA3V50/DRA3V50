from PIL import Image, ImageDraw

# Simple placeholder SVG generator to test workflow
SVG_FILE = "dashboard.svg"

width, height = 600, 400
bg_color = "#0B1E3F"
text_color = "#00FFFF"

# Create basic SVG
svg_content = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="{bg_color}"/>
  <text x="50%" y="50%" fill="{text_color}" font-size="24" font-family="Arial" text-anchor="middle" alignment-baseline="middle">
    SOC / IR / SIEM / SOAR / EDR / Data Dashboard
  </text>
</svg>'''

# Write SVG to file
with open(SVG_FILE, "w") as f:
    f.write(svg_content)

print(f"Generated {SVG_FILE}")

