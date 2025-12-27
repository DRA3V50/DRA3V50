import svgwrite

dwg = svgwrite.Drawing('mitre_dashboard.svg', size=("900px", "500px"))

# Background
dwg.add(dwg.rect((0, 0), ("900px", "500px"), fill="#040404"))

# Title: Name & Role
title = dwg.text(
    "Dany Arabo - Data Analyst (FBI/Threat Intel)",
    insert=("40px", "60px"),
    fill="#18FF00",
    font_size="28px",
    font_weight="bold"
)

# Simple glow filter
filter_glow = dwg.defs.add(dwg.filter(id="glow"))
filter_glow.feGaussianBlur(in_="SourceGraphic", stdDeviation=3, result="blur")
filter_glow.feMerge(layernames=["blur", "SourceGraphic"])
title['filter'] = "url(#glow)"
dwg.add(title)

# Key Skills / MITRE Techniques
techniques = [
    "TA0001 Initial Access",
    "TA0002 Execution",
    "TA0003 Persistence",
    "TA0004 Privilege Escalation",
]

dwg.add(dwg.text("Core Skills / MITRE Techniques:", insert=("40px", 120), fill="#18FF00", font_size="22px"))

y = 160
for i, t in enumerate(techniques):
    text = dwg.text(t, insert=("60px", f"{y + i*30}px"), fill="white", font_size="18px")
    dwg.add(text)
    # Subtle glow animation
    text.add(dwg.animate(attributeName="fill", values="white;#18FF00;white", dur=f"{1.5 + i*0.2}s", repeatCount="indefinite"))

# Certifications / Achievements
certs = [
    "Intro to Networking & Cloud Computing",
    "Intro to OS & Security"
]

dwg.add(dwg.text("Certifications / Achievements:", insert=("500px", 120), fill="#18FF00", font_size="22px"))

y_cert = 160
for i, c in enumerate(certs):
    text = dwg.text(c, insert=("520px", f"{y_cert + i*30}px"), fill="white", font_size="18px")
    dwg.add(text)
    # Subtle color pulse
    text.add(dwg.animate(attributeName="fill", values="white;#00FFFF;white", dur=f"{1.7 + i*0.2}s", repeatCount="indefinite"))

dwg.save()
