import random
import os
from datetime import datetime, timedelta

os.makedirs("assets", exist_ok=True)

# Example live threat feed
threats = [
    {
        "title": "Ransomware Activity",
        "desc": "New Conti variant targeting healthcare sector",
        "severity": "Critical",
        "time": "15 min ago",
        "region": "Global",
        "color": "#ff4e4e"
    },
    {
        "title": "Phishing Campaign",
        "desc": "Microsoft 365 credential harvesting emails",
        "severity": "High",
        "time": "42 min ago",
        "region": "North America",
        "color": "#ffb74e"
    },
    {
        "title": "Vulnerability Alert",
        "desc": "CVE-2023-1234: Apache Log4j new vulnerability",
        "severity": "Medium",
        "time": "2 hours ago",
        "region": "Global",
        "color": "#4effff"
    }
]

# Live security dashboard stats
siem = random.randint(10, 30)
edr = random.randint(5, 20)
soar = random.randint(3, 10)

# Start SVG
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="300">
<rect width="600" height="300" fill="#0a0f1a"/>
<text x="20" y="30" font-family="Consolas, monospace" font-size="16" fill="#a0c8ff">Threat Feed</text>
'''

y_offset = 60
for t in threats:
    svg += f'''
    <rect x="20" y="{y_offset-15}" width="560" height="35" rx="5" ry="5" fill="#1a2132"/>
    <circle cx="40" cy="{y_offset+2}" r="6" fill="{t['color']}">
        <animate attributeName="r" values="6;10;6" dur="2s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="55" y="{y_offset}" font-family="Consolas, monospace" font-size="12" fill="#ffffff">{t['title']}</text>
    <text x="55" y="{y_offset+15}" font-family="Consolas, monospace" font-size="10" fill="#a0c8ff">{t['desc']} ({t['severity']}, {t['time']}, {t['region']})</text>
    '''
    y_offset += 50

# Live security dashboard stats
svg += f'''
<text x="20" y="{y_offset}" font-family="Consolas, monospace" font-size="16" fill="#a0c8ff">Live Security Dashboard</text>

<text x="40" y="{y_offset+25}" font-family="Consolas, monospace" font-size="12" fill="#ff4e4e">SIEM Alerts: {siem} New</text>
<text x="40" y="{y_offset+45}" font-family="Consolas, monospace" font-size="12" fill="#ffb74e">EDR Events: {edr} New</text>
<text x="40" y="{y_offset+65}" font-family="Consolas, monospace" font-size="12" fill="#4effff">SOAR Actions: {soar} Active</text>
'''

svg += "</svg>"

with open("assets/live_threat_feed.svg", "w") as f:
    f.write(svg)

print("✅ Live threat feed SVG updated!")
