import svgwrite

dwg = svgwrite.Drawing('mitre_dashboard.svg', size=("900px", "500px"))

# Background
dwg.add(dwg.rect((0, 0), ("900px", "500px"), fill="#0a0f14"))  # dark navy background

# Name & Role
name_role = dwg.text(
    "Dany Arabo - Cybersecurity / Blue Team Analyst",
    insert=("40px", "60px"),
    fill="#00d8ff",
    font_size="28px",
    font_weight="bold"
)
dwg.add(name_role)

# Glow filter for subtle animation
filter_glow = dwg.defs.add(dwg.filter(id="glow"))
filter_glow.feGaussianBlur(in_="SourceGraphic", stdDeviation=2, result="blur")
filter_glow.feMerge(layernames=["blur", "SourceGraphic"])
name_role['filter'] = "url(#glow)"

# Core Blue Team Skills / Techniques
skills = [
    "SIEM Monitoring & Analysis",
    "EDR / Endpoint Threat Hunting",
    "Log Analysis & Correlation",
    "Incident Response",
    "Cloud Security Monitoring",
    "Vulnerability & Patch Management"
]

dwg.add(dwg.text("Core Blue Team Skills:", insert=("40px", 120), fill="#00d8ff", font_size="22px"))

y = 160
for i, s in enumerate(skills):
    text = dwg.text(s, insert=("60px", f"{y + i*30}px"), fill="#a0e0ff", font_size="18px")
    dwg.add(text)
    # subtle color pulse animation
    text.add(dwg.animate(attributeName="fill",
                         values=f"#a0e0ff;#00d8ff;#a0e0ff",
                         dur=f"{1.5 + i*0.2}s",
                         repeatCount="indefinite"))

# Optional: Certifications / Achievements
certs = [
    "Certified SOC Analyst",
    "CrowdStrike & Splunk Experience",
    "Penetration Testing Foundations"
]

dwg.add(dwg.text("Certifications / Achievements:", insert=("500px", 120), fill="#00d8ff", font_size="22px"))

y_cert = 160
for i, c in enumerate(certs):
    text = dwg.text(c, insert=("520px", f"{y_cert + i*30}px"), fill="#a0e0ff", font_size="18px")
    dwg.add(text)
    text.add(dwg.animate(attributeName="fill",
                         values=f"#a0e0ff;#00d8ff;#a0e0ff",
                         dur=f"{1.7 + i*0.2}s",
                         repeatCount="indefinite"))

dwg.save()

