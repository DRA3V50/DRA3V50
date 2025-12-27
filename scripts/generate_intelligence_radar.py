from datetime import datetime

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
     width="300" height="300" viewBox="0 0 300 300">

  <rect width="100%" height="100%" fill="#0b0f14"/>

  <!-- Radar circle -->
  <circle cx="150" cy="150" r="120"
          stroke="#00ffcc"
          stroke-width="2"
          fill="none"/>

  <!-- Sweep line -->
  <line x1="150" y1="150" x2="150" y2="30"
        stroke="#00ffcc"
        stroke-width="2">
    <animateTransform
      attributeName="transform"
      type="rotate"
      from="0 150 150"
      to="360 150 150"
      dur="4s"
      repeatCount="indefinite"/>
  </line>

  <!-- Center dot -->
  <circle cx="150" cy="150" r="4" fill="#00ffcc"/>

  <!-- Labels -->
  <text x="20" y="280"
        fill="#e0e0e0"
        font-family="monospace"
        font-size="10">
    Last Update: {datetime.utcnow().isoformat()}Z
  </text>

</svg>
'''

with open("assets/intelligence_radar.svg", "w", encoding="utf-8") as f:
    f.write(svg)
