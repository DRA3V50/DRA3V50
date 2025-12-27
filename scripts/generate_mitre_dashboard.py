import svgwrite

dwg = svgwrite.Drawing('mitre_dashboard.svg', size=("900px", "550px"))

# Background
dwg.add(dwg.rect((0, 0), ("900px", "550px"), fill="#040404"))

# Title
dwg.add(dwg.text(
    "MITRE ATT&CK DASHBOARD",
    insert=("40px", "80px"),
    fill="#18FF00",
    font_size="34px"
))

# MITRE Techniques
techniques = [
    "TA0001 Initial Access",
    "TA0002 Execution",
    "TA0003 Persistence",
    "TA0004 Privilege Escalation",
    "TA0005 Defense Evasion"
]

y = 150
for i, t in enumerate(techniques):
    text = dwg.text(t, insert=("60px", f"{y}px"), fill="white", font_size="20px")
    dwg.add(text)
    
    # Add pulsing color animation
    text.add(dwg.animate(
        attributeName="fill",
        values="white;#18FF00;white",
        dur=f"{1.5 + i*0.3}s",  # slightly staggered for effect
        repeatCount="indefinite"
    ))
    
    y += 50

dwg.save()
