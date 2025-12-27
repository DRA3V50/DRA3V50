import svgwrite

dwg = svgwrite.Drawing('mitre_dashboard.svg', size=("800px", "500px"))

dwg.add(dwg.rect(insert=(0, 0), size=("800px", "500px"),
                 fill="black"))

dwg.add(dwg.text("MITRE ATT&CK DASHBOARD",
                 insert=(40, 80),
                 fill="white",
                 font_size="32px"))

dwg.add(dwg.text("Example Technique Coverage",
                 insert=(40, 140),
                 fill="white",
                 font_size="20px"))

techniques = [
    "TA0001 Initial Access",
    "TA0002 Execution",
    "TA0003 Persistence",
    "TA0004 Privilege Escalation",
    "TA0005 Defense Evasion"
]

y = 200
for t in techniques:
    dwg.add(dwg.text(t, insert=(60, y), fill="white", font_size="18px"))
    y += 40

dwg.save()

print("MITRE dashboard generated!")

