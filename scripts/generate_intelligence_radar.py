from datetime import datetime

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
     width="800" height="200" viewBox="0 0 800 200">

  <rect width="100%" height="100%" fill="#0b0f14"/>

  <text x="20" y="40"
        fill="#00ffcc"
        font-family="monospace"
        font-size="20">
    Intelligence Activity Radar
  </text>

  <text x="20" y="90"
        fill="#e0e0e0"
        font-family="monospace"
        font-size="14">
    Last Updated: {datetime.utcnow().isoformat()}Z
  </text>

</svg>
'''

with open("assets/intelligence_radar.svg", "w", encoding="utf-8") as f:
    f.write(svg)
