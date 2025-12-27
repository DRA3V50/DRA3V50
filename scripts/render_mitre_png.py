import cairosvg
import os

SVG_PATH = "assets/mitre.svg"
PNG_PATH = "assets/mitre.png"

if not os.path.exists(SVG_PATH):
    raise FileNotFoundError(f"{SVG_PATH} not found")

cairosvg.svg2png(
    url=SVG_PATH,
    write_to=PNG_PATH,
    output_width=1200
)

print("✔ MITRE PNG rendered:", PNG_PATH)
