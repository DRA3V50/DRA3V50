import svgwrite

dwg = svgwrite.Drawing('mitre_dashboard.svg', size=("900px", "550px"))

# Background
dwg.add(dwg.rect((0, 0), ("900px", "550px"), fill="#040404"))

# Title with glow
title = dwg.text(
    "MITRE ATT&CK DASHBOARD",
    insert=("40px", "80px"),
    fill="#18FF00",
    font_size="34px"
)
# Add pulsating glow using SVG filter
filter_glow = dwg.defs.add(dwg.filter(id="glow"))
filter_glow.feGaussianBlur(in_="SourceGraphic", stdDeviation=4, result="blur")
filter_glow.feMerge().feMergeNode(in_="blur")
filter_glow.feMerge().feMergeNode(in_="SourceGraphic")
title['filter'] = "url(#glow)"
dwg.add(title)

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
    
    # Pulsing color animation
    text.add(dwg.animate(
        attributeName="fill",
        values="white;#18FF00;white",
        dur=f"{1.5 + i*0.3}s",
        repeatCount="indefinite"
    ))
    
    # Subtle vertical movement to mimic "flow"
    text.add(dwg.animateTransform(
        attributeName="transform",
        type="translate",
        values="0 0;0 3;0 0",
        dur=f"{2 + i*0.3}s",
        repeatCount="indefinite"
    ))
    
    # Optional glow effect
    glow = dwg.text(t, insert=("60px", f"{y}px"), fill="#18FF00", font_size="20px", opacity=0.3)
    glow['filter'] = "url(#glow)"
    dwg.add(glow)
    
    y += 50

dwg.save()
