import svgwrite

dwg = svgwrite.Drawing('mitre_dashboard.svg', size=("900px", "550px"))

dwg.add(dwg.rect((0, 0), ("900px", "550px"), fill="#040404"))

dwg.add(dwg.text(
    "MITRE ATT&CK DASHBOARD",
    insert=("40px", "80px"),
    fill="#18FF00",
    font_size="34px"
))

techniques = [
    "TA0001 Initial Access",
    "TA0002 Execution",
    "TA0003 Persistence",
    "TA0004 Privilege Escalation",
    "TA0005 Defense Evasion"
]

y = 150
for t in techniques:
    dwg.add(dwg.text(t, insert=("60px", f"{y}px"),
                     fill="white", font_size="20px"))
    y += 50

dwg.save()
