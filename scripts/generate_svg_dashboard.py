import subprocess
import datetime

SVG_FILE = "dashboard.svg"
WIDTH = 800
HEIGHT = 400
BG_COLOR = "#0B1E3F"
DOMAIN_COLORS = {
    "SOC": "#00FFFF",
    "IR": "#00AFFF",
    "SIEM": "#0088FF",
    "SOAR": "#0055FF",
    "EDR": "#0022FF",
    "Data": "#00FFD0"
}

# Map keywords to domains
DOMAIN_MAP = {
    "SOC": ["alert", "ticket", "monitor", "triage"],
    "IR": ["incident", "containment", "forensics", "report"],
    "SIEM": ["splunk", "sentinel", "rule", "log"],
    "SOAR": ["automation", "playbook", "workflow"],
    "EDR": ["crowdstrike", "defender", "endpoint", "scan"],
    "Data": ["analytics", "dashboard", "report", "python", "sql"]
}

# Initialize counts
domain_counts = {domain: 0 for domain in DOMAIN_MAP}

# Get last 50 commits
try:
    commit_messages = subprocess.check_output(
        ["git", "log", "--pretty=%s", "-n", "50"], encoding="utf-8"
    ).split("\n")
except Exception as e:
    print("Error reading git commits:", e)
    commit_messages = []

# Count commits per domain
for msg in commit_messages:
    msg_lower = msg.lower()
    for domain, keywords in DOMAIN_MAP.items():
        if any(keyword in msg_lower for keyword in keywords):
            domain_counts[domain] += 1

# Generate SVG
svg_lines = [
    f'<svg width="{WIDTH}" height="{HEIGHT}" xmlns="http://www.w3.org/2000/svg">',
    f'<rect width="100%" height="100%" fill="{BG_COLOR}"/>',
    f'<text x="{WIDTH/2}" y="40" fill="#FFFFFF" font-size="28" font-family="Arial" text-anchor="middle">SOC Dashboard</text>'
]

# Draw bars for each domain
bar_width = 80
gap = 30
start_x = 50
max_count = max(domain_counts.values()) or 1
for i, (domain, count) in enumerate(domain_counts.items()):
    bar_height = (count / max_count) * (HEIGHT - 150)
    x = start_x + i * (bar_width + gap)
    y = HEIGHT - bar_height - 50
    color = DOMAIN_COLORS[domain]
    svg_lines.append(f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{color}" rx="8" ry="8"/>')
    svg_lines.append(f'<text x="{x + bar_width/2}" y="{HEIGHT - 30}" fill="#FFFFFF" font-size="14" font-family="Arial" text-anchor="middle">{domain} ({count})</text>')

# Timestamp
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
svg_lines.append(f'<text x="{WIDTH-10}" y="{HEIGHT-10}" fill="#AAAAAA" font-size="12" font-family="Arial" text-anchor="end">Updated: {now}</text>')

svg_lines.append("</svg>")

# Write SVG file
with open(SVG_FILE, "w") as f:
    f.write("\n".join(svg_lines))

print(f"Generated {SVG_FILE}")
