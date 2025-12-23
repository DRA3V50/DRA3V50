import subprocess
import datetime
import random

SVG_FILE = "dashboard.svg"
WIDTH = 1000
HEIGHT = 600
BG_COLOR = "#0B1E3F"
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# Domains & colors
DOMAINS = ["SOC", "IR", "SIEM", "SOAR", "EDR", "Data"]
DOMAIN_COLORS = {
    "SOC": "#00FFFF",
    "IR": "#FFD700",
    "SIEM": "#0088FF",
    "SOAR": "#8000FF",
    "EDR": "#00FF66",
    "Data": "#00FFD0"
}

DOMAIN_KEYWORDS = {
    "SOC": ["alert", "ticket", "monitor", "triage"],
    "IR": ["incident", "contain", "forensic", "report"],
    "SIEM": ["splunk", "sentinel", "log", "rule"],
    "SOAR": ["automation", "playbook", "workflow"],
    "EDR": ["crowdstrike", "defender", "endpoint", "scan"],
    "Data": ["analytics", "dashboard", "python", "sql"]
}

# Initialize counts
domain_counts = {d: {"done":0, "ongoing":0, "pending":0} for d in DOMAINS}

# --- Pull last 50 commits ---
try:
    commit_messages = subprocess.check_output(
        ["git", "log", "--pretty=%s", "-n", "50"], encoding="utf-8"
    ).split("\n")
except:
    commit_messages = []

# --- Map commits to domains ---
for msg in commit_messages:
    msg_lower = msg.lower()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(k in msg_lower for k in keywords):
            domain_counts[domain]["done"] += 1

# Simulate ongoing/pending (replace with real GitHub workflow status later)
for d in DOMAINS:
    domain_counts[d]["ongoing"] = random.randint(0,2)
    domain_counts[d]["pending"] = random.randint(0,2)

# --- Generate SVG ---
svg = [
    f'<svg width="{WIDTH}" height="{HEIGHT}" xmlns="http://www.w3.org/2000/svg">',
    f'<rect width="100%" height="100%" fill="{BG_COLOR}"/>',
    f'<text x="{WIDTH/2}" y="40" fill="#FFFFFF" font-size="28" font-family="Arial" text-anchor="middle">Ultimate SOC Hybrid Dashboard</text>'
]

# --- Draw Tiles on left ---
tile_width = 140
tile_height = 100
gap = 20
start_x = 20
start_y = 80

for i, d in enumerate(DOMAINS):
    x = start_x
    y = start_y + i * (tile_height + gap)
    counts = domain_counts[d]
    color = DOMAIN_COLORS[d]

    # Tile rectangle
    svg.append(f'<rect x="{x}" y="{y}" width="{tile_width}" height="{tile_height}" rx="12" ry="12" fill="#112B4C"/>')
    # Domain title
    svg.append(f'<text x="{x+tile_width/2}" y="{y+20}" fill="{color}" font-size="18" font-family="Arial" text-anchor="middle">{d}</text>')
    # Status
    svg.append(f'<text x="{x+10}" y="{y+50}" fill="#FFFFFF" font-size="14" font-family="Arial">✅ Done: {counts["done"]}</text>')
    svg.append(f'<text x="{x+10}" y="{y+70}" fill="#FFD700" font-size="14" font-family="Arial">⚠️ Ongoing: {counts["ongoing"]}</text>')
    svg.append(f'<text x="{x+10}" y="{y+90}" fill="#FF4500" font-size="14" font-family="Arial">❌ Pending: {counts["pending"]}</text>')

# --- Draw Radar Orbit on right ---
radius_base = 60
blip_count = 5

for i, d in enumerate(DOMAINS):
    ring_radius = radius_base + i*40
    svg.append(f'<circle cx="{CENTER_X+200}" cy="{CENTER_Y}" r="{ring_radius}" fill="none" stroke="{DOMAIN_COLORS[d]}" stroke-width="1" opacity="0.4"/>')
    # Orbiting blips
    for j in range(blip_count):
        angle = random.randint(0, 360)
        svg.append(f'''
        <circle cx="{CENTER_X+200}" cy="{CENTER_Y}" r="6" fill="{DOMAIN_COLORS[d]}">
            <animateTransform attributeName="transform" attributeType="XML"
                type="rotate" from="0 {CENTER_X+200} {CENTER_Y}" to="360 {CENTER_X+200} {CENTER_Y}"
                dur="{10 + j*2}s" repeatCount="indefinite"/>
            <animate attributeName="r" values="6;12;6" dur="2s" repeatCount="indefinite"/>
        </circle>
        ''')

# Timestamp
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
svg.append(f'<text x="{WIDTH-10}" y="{HEIGHT-10}" fill="#AAAAAA" font-size="12" font-family="Arial" text-anchor="end">Updated: {now}</text>')

svg.append("</svg>")

with open(SVG_FILE, "w") as f:
    f.write("\n".join(svg))

print(f"Generated {SVG_FILE}")
