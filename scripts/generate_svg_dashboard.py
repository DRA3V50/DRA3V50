import subprocess
import datetime
import json

SVG_FILE = "dashboard.svg"
WIDTH = 900
HEIGHT = 500
BG_COLOR = "#0B1E3F"

# Domains and colors
DOMAINS = ["SOC", "IR", "SIEM", "SOAR", "EDR", "Data"]
DOMAIN_COLORS = {
    "SOC": "#00FFFF",
    "IR": "#FFD700",
    "SIEM": "#0088FF",
    "SOAR": "#8000FF",
    "EDR": "#00FF66",
    "Data": "#00FFD0"
}

# Keywords for each domain (to detect commits/PRs)
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

# ----- Step 1: Pull last 50 commit messages -----
try:
    commit_messages = subprocess.check_output(
        ["git", "log", "--pretty=%s", "-n", "50"], encoding="utf-8"
    ).split("\n")
except Exception as e:
    print("Error reading commits:", e)
    commit_messages = []

# ----- Step 2: Map commits to domains -----
for msg in commit_messages:
    msg_lower = msg.lower()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(k in msg_lower for k in keywords):
            domain_counts[domain]["done"] += 1

# ----- Step 3: Randomly simulate ongoing/pending for demonstration -----
# In future, you can pull issues or workflow runs for real statuses
import random
for d in DOMAINS:
    domain_counts[d]["ongoing"] = random.randint(0,2)
    domain_counts[d]["pending"] = random.randint(0,2)

# ----- Step 4: Generate SVG -----
svg_lines = [
    f'<svg width="{WIDTH}" height="{HEIGHT}" xmlns="http://www.w3.org/2000/svg">',
    f'<rect width="100%" height="100%" fill="{BG_COLOR}"/>',
    f'<text x="{WIDTH/2}" y="40" fill="#FFFFFF" font-size="28" font-family="Arial" text-anchor="middle">Ultimate SOC Dashboard</text>'
]

# Draw domain bars + pulsing dots
bar_width = 80
gap = 30
start_x = 50
max_total = max(sum(domain_counts[d].values()) for d in DOMAINS) or 1
for i, d in enumerate(DOMAINS):
    total = sum(domain_counts[d].values())
    bar_height = (total / max_total) * (HEIGHT - 150)
    x = start_x + i * (bar_width + gap)
    y = HEIGHT - bar_height - 50
    color = DOMAIN_COLORS[d]
    # Main bar
    svg_lines.append(f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{color}" rx="8" ry="8"/>')
    # Pulsing dot for new activity
    svg_lines.append(f'''
        <circle cx="{x + bar_width/2}" cy="{y}" r="8" fill="#FFFFFF">
            <animate attributeName="r" values="8;14;8" dur="1.5s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="1;0.5;1" dur="1.5s" repeatCount="indefinite"/>
        </circle>
    ''')
    # Status text
    counts = domain_counts[d]
    svg_lines.append(f'<text x="{x + bar_width/2}" y="{HEIGHT - 30}" fill="#FFFFFF" font-size="14" font-family="Arial" text-anchor="middle">{d}: ✅{counts["done"]} ⚠️{counts["ongoing"]} ❌{counts["pending"]}</text>')

# Timestamp
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
svg_lines.append(f'<text x="{WIDTH-10}" y="{HEIGHT-10}" fill="#AAAAAA" font-size="12" font-family="Arial" text-anchor="end">Updated: {now}</text>')

svg_lines.append("</svg>")

with open(SVG_FILE, "w") as f:
    f.write("\n".join(svg_lines))

print(f"Generated {SVG_FILE}")
