import os
import cairosvg

if not os.path.exists("assets/mitre.svg"):
    raise FileNotFoundError("SVG file does not exist. Run build_mitre_svg.py first.")

cairosvg.svg2png(
    url="assets/mitre.svg",
    write_to="assets/mitre.png",
    output_width=800
)
