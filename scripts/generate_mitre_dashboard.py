import svgwrite
import json

# Example JSON file with MITRE coverage percentages
# Replace with your actual coverage data or update JSON file regularly
coverage_data = {
    "Initial Access": 80,
    "Execution": 65,
    "Persistence": 90,
    "Privilege Escalation": 70,
    "Defense Evasion": 50
}

# Compact Blue Team skills and certifications
skills = ["SIEM Monitoring", "EDR / Threat Hunting", "Log Analysis", "Incident Response"]
certs = ["Certified SOC Analyst", "CrowdStrike & Splunk", "Pen Testing Foundations"]

dwg = svgwrite.Drawing('mitre_dashboard.svg', size=("700px", "400px"))

# Background
dwg.add(dwg.rect((0, 0), ("700px", "400px"), fill="#0a0f14"))

# Name & Role (compact header)
dwg.add(dwg.text("Dany Arabo - Blue Team Analyst",
                 insert=(20, 40), fill="#00d8ff", font_size="22px", font_weight="bold"))

# Glow filter for animation
filter_glow = dwg.defs.add(dwg.filter(id="glow"))
filter_glow.feGaussianBlur(in_="SourceGraphic", stdDeviation=2, result="blur")
filter_glow.feMerge(layernames=["blur", "SourceGraphic"])

# MITRE ATT&CK Coverage (compact bars)
dwg.add(dwg.text("MITRE ATT&CK Coverage:", insert=(20, 70), fill="#00d8ff", font_size="16px"))

x_bar_start = 20
y_bar_start = 90
bar_width = 250
bar_height = 15
bar_spacing = 30

for i, (tactic, percent) in enumerate(coverage_data.items()):
    # Tactic label
    dwg.add(dwg.text(tactic, insert=(x_bar_start, y_bar_start + i*bar_spacing + 12),
                     fill="#a0e0ff", font_size="14px"))
    
    # Background bar
    dwg.add(dwg.rect(insert=(x_bar_start + 120, y_bar_start + i*bar_spacing),
                     size=(bar_width, bar_height), fill="#1a2a3a", rx=3, ry=3))
    
    # Coverage bar with subtle pulse animation
    bar = dwg.rect(insert=(x_bar_start + 120, y_bar_start + i*bar_spacing),
                   size=(bar_width * percent / 100, bar_height), fill="#00d8ff", rx=3, ry=3)
    dwg.add(bar)
    bar.add(dwg.animate(attributeName="fill", values="#00d8ff;#80f0ff;#00d8ff",
                        dur=f"{1.5 + i*0.2}s", repeatCount="indefinite"))

# Skills (compact right column)
dwg.add(dwg.text("Skills:", insert=(400, 70), fill="#00d8ff", font_size="16px"))
for i, skill in enumerate(skills):
    text = dwg.text(skill, insert=(420, 90 + i*20), fill="#a0e0ff", font_size="14px")
    dwg.add(text)
    text.add(dwg.animate(attributeName="fill", values="#a0e0ff;#00d8ff;#a0e0ff",
                         dur=f"{1.6 + i*0.2}s", repeatCount="indefinite"))

# Certifications (below skills)
dwg.add(dwg.text("Certifications:", insert=(400, 170), fill="#00d8ff", font_size="16px"))
for i, cert in enumerate(certs):
    text = dwg.text(cert, insert=(420, 190 + i*20), fill="#a0e0ff", font_size="14px")
    dwg.add(text)
    text.add(dwg.animate(attributeName="fill", values="#a0e0ff;#00d8ff;#a0e0ff",
                         dur=f"{1.7 + i*0.2}s", repeatCount="indefinite"))

dwg.save()
