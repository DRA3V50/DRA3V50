from pathlib import Path

Path("assets").mkdir(exist_ok=True)

# SOC-relevant MITRE tactics only
tactics = ["Reconnaissance", "Initial Access", "Persistence",
           "Privilege Escalation", "Defense Evasion", "Credential Access",
           "Lateral Movement", "Exfiltration", "Impact"]
coverage = [0.8, 0.6, 0.5, 0.6, 0.9, 0.4, 0.5, 0.6, 0.3]  # 0.0 to 1.0

width = 600
bar_height = 40
bar_spacing = 25

svg_elements = []

# SVG header
svg_elements.append(f'<svg width="{width}" height="{(bar_height + bar_spacing)*len(tactics) + 50}" xmlns="http://www.w3.org/2000/svg">')
svg_elements.append('<style> .bar-bg { fill:#323232; } .bar-fill { fill:#0078FF; animation: fill 2s forwards; } text { fill:white; font-family:Arial, sans-serif; font-size:14px;} @keyframes fill { from { width:0; } to { width:1; } } </style>')

for i, (tactic, cov) in enumerate(zip(tactics, coverage)):
    y = i*(bar_height + bar_spacing) + 20
    x0 = 180
    bar_width = cov * 250  # max width

    # Bar background
    svg_elements.append(f'<rect x="{x0}" y="{y}" width="250" height="{bar_height}" class="bar-bg"/>')

    # Animated fill bar using CSS animation
    svg_elements.append(f'''
    <rect x="{x0}" y="{y}" width="0" height="{bar_height}" class="bar-fill">
        <animate attributeName="width" from="0" to="{bar_width}" dur="1.5s" fill="freeze"/>
    </rect>
    ''')

    # Tactic label
    svg_elements.append(f'<text x="10" y="{y + bar_height*0.7}">{tactic}</text>')

    # Percentage label
    svg_elements.append(f'<text x="{x0 + bar_width + 10}" y="{y + bar_height*0.7}">{int(cov*100)}%</text>')

svg_elements.append('</svg>')

# Save SVG
svg_path = "assets/mitre_bar_chart.svg"
with open(svg_path, "w") as f:
    f.write("\n".join(svg_elements))

print(f"MITRE Bar Chart SVG generated at {svg_path}")
