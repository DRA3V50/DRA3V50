import svgwrite

# Example MITRE ATT&CK coverage data (replace with real coverage)
coverage = {
    "Initial Access": 80,
    "Execution": 65,
    "Persistence": 90,
    "Privilege Escalation": 70,
    "Defense Evasion": 50,
    "Credential Access": 60
}

# Blue team skills
skills = [
    "SIEM Monitoring & Analysis",
    "EDR / Endpoint Threat Hunting",
    "Log Analysis & Correlation",
    "Incident Response",
    "Cloud Security Monitoring"
]

# Certifications / Achievements
certs = [
    "Certified SOC Analyst",
    "CrowdStrike & Splunk Experience",
    "Penetration Testing Foundations"
]

dwg = svgwrite.Drawing('mitre_dashboard.svg', size=("1000px", "600px"))

# Background
dwg.add(dwg.rect((0, 0), ("1000px", "600px"), fill="#0a0f14"))

# Header: name & role
dwg.add(dwg.text(
    "Dany Arabo - Cybersecurity / Blue Team Analyst",
    insert=("40px", "50px"),
    fill="#00d8ff",
    font_size="28px",
    font_weight="bold"
))

# Glow filter for animation
filter_glow = dwg.defs.add(dwg.filter(id="glow"))
filter_glow.feGaussianBlur(in_="SourceGraphic", stdDeviation=2, result="blur")
filter_glow.feMerge(layernames=["blur", "SourceGraphic"])

# MITRE ATT&CK Coverage Section
dwg.add(dwg.text("MITRE ATT&CK Coverage:", insert=("40px", 100), fill="#00d8ff", font_size="22px"))

x_start = 60
y_start = 130
bar_width = 200
bar_height = 20
bar_spacing = 40

for i, (tactic, percent) in enumerate(coverage.items()):
    # Label
    dwg.add(dwg.text(tactic, insert=(x_start, y_start + i*bar_spacing), fill="#a0e0ff", font_size="18px"))
    
    # Background bar
    dwg.add(dwg.rect(
        insert=(x_start + 200, y_start + i*bar_spacing - 15),
        size=(bar_width, bar_height),
        fill="#1a2a3a",
        rx=5, ry=5
    ))
    
    # Coverage bar with animation (glow effect)
    bar = dwg.rect(
        insert=(x_start + 200, y_start + i*bar_spacing - 15),
        size=(bar_width * percent / 100, bar_height),
        fill="#00d8ff",
        rx=5, ry=5
    )
    dwg.add(bar)
    bar.add(dwg.animate(attributeName="fill", values="#00d8ff;#80f0ff;#00d8ff", dur=f"{1.5 + i*0.2}s", repeatCount="indefinite"))

# Core Blue Team Skills Section
dwg.add(dwg.text("Core Blue Team Skills:", insert=("40px", 370), fill="#00d8ff", font_size="22px"))
y_skills = 410
for i, s in enumerate(skills):
    text = dwg.text(s, insert=("60px", y_skills + i*30), fill="#a0e0ff", font_size="18px")
    dwg.add(text)
    text.add(dwg.animate(attributeName="fill", values="#a0e0ff;#00d8ff;#a0e0ff", dur=f"{1.5 + i*0.2}s", repeatCount="indefinite"))

# Certifications / Achievements Section
dwg.add(dwg.text("Certifications / Achievements:", insert=("500px", 370), fill="#00d8ff", font_size="22px"))
y_cert = 410
for i, c in enumerate(certs):
    text = dwg.text(c, insert=("520px", y_cert + i*30), fill="#a0e0ff", font_size="18px")
    dwg.add(text)
    text.add(dwg.animate(attributeName="fill", values="#a0e0ff;#00d8ff;#a0e0ff", dur=f"{1.7 + i*0.2}s", repeatCount="indefinite"))

dwg.save()
