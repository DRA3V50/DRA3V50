import random
from datetime import datetime

# Hosts with their MITRE ATT&CK stage
hosts = [
    {"name": "HostA", "stage": "Initial Access"},
    {"name": "Server42", "stage": "Execution"},
    {"name": "Workstation12", "stage": "Persistence"},
    {"name": "Firewall", "stage": "Defense Evasion"},
    {"name": "DBServer", "stage": "Privilege Escalation"}
]

# Generate random activity for each host
for host in hosts:
    host["activity"] = random.randint(10, 100)  # intensity 10-100

# Start SVG
svg_header = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400">
<rect width="600" height="400" fill="#0a0f1a"/>
<defs>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
<feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#4effff" flood-opacity="0.8"/>
</filter>
</defs>
'''

# Animated circles per host
svg_circles = ""
for i, host in enumerate(hosts):
    x = 100 + i * 90
    y = 200
    r = 6
    max_r = 6 + host["activity"] // 10  # bigger radius for higher activity
    dur = round(2 + random.random() * 2, 2)  # random pulse duration
    opacity = round(0.3 + host["activity"] / 150, 2)
    svg_circles += f'''
    <circle cx="{x}" cy="{y}" r="{r}" fill="#4effff" filter="url(#glow)" opacity="{opacity}">
        <animate attributeName="r" values="{r};{max_r};{r}" dur="{dur}s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="{opacity};1;{opacity}" dur="{dur}s" repeatCount="indefinite"/>
        <title>{host['name']} - {host['stage']}</title>
    </circle>
    <text x="{x + 10}" y="{y + 5}" font-family="Consolas, monospace" font-size="12" fill="#a0c8ff">{host['name']}</text>
    '''

# Optional "FBI eye" in corner
svg_eye = '''
<circle cx="550" cy="50" r="20" fill="none" stroke="#4effff" stroke-width="2">
    <animate attributeName="r" values="20;25;20" dur="3s" repeatCount="indefinite"/>
</circle>
<circle cx="550" cy="50" r="8" fill="#4effff">
    <animate attributeName="r" values="8;12;8" dur="2.5s" repeatCount="indefinite"/>
</circle>
'''

# Footer with timestamp
svg_footer = f'''
<text x="10" y="390" font-family="Consolas, monospace" font-size="10" fill="#5cb3ff">
Last updated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC
</text>
</svg>
'''

# Write SVG file
svg_content = svg_header + svg_circles + svg_eye + svg_footer

with open("../assets/cyber_heatmap_live.svg", "w") as f:
    f.write(svg_content)

print("SVG threat heatmap generated successfully!")

