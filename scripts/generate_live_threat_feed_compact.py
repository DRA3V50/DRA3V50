import random
import os

# Ensure assets folder exists
os.makedirs("assets", exist_ok=True)

# Canvas dimensions
WIDTH = 300
HEIGHT = 200

threats = [
    {"name": "Ransomware", "severity": "Critical"},
    {"name": "Phishing", "severity": "High"},
    {"name": "Vulnerability", "severity": "Medium"}
]

# Map severity to color
severity_color = {
    "Critical": "#ff4e4e",
    "High": "#ffb74e",
    "Medium": "#4effff"
}

# Random counts for live updates (simulate real-time)
for t in threats:
    t["count"] = random.randint(1, 25)

with open("assets/live_threat_chart.svg", "w") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}">\n')
    f.write(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#0a0f1a"/>\n')
    f.write('<text x="10" y="20" font-family="Consolas, monospace" font-size="12" fill="#a0c8ff">Live Threat Chart</text>\n')
    
    # Draw horizontal animated bars
    x_start = 10
    y_start = 40
    bar_height = 20
    spacing = 30
    max_bar_width = WIDTH - 60
    
    for t in threats:
        bar_width = t["count"] / 25 * max_bar_width  # scale to max width
        f.write(f'<rect x="{x_start}" y="{y_start}" width="{bar_width}" height="{bar_height}" fill="{severity_color[t["severity"]]}">\n')
        f.write(f'<animate attributeName="width" values="0;{bar_width};0" dur="2s" repeatCount="indefinite"/>\n')
        f.write('</rect>\n')
        f.write(f'<text x="{x_start + bar_width + 5}" y="{y_start + 14}" font-family="Consolas, monospace" font-size="10" fill="#ffffff">{t["name"]} ({t["count"]})</text>\n')
        y_start += spacing

    f.write('</svg>')

print("Live Threat Chart SVG generated successfully!")
