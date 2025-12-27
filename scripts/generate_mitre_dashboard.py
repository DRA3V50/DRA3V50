import svgwrite

dwg = svgwrite.Drawing('mitre_dashboard.svg', size=("1000px", "600px"))

# Background
dwg.add(dwg.rect((0, 0), ("1000px", "600px"), fill="#040404"))

# Title with glow
title = dwg.text(
    "FBI SOC MITRE DASHBOARD",
    insert=("40px", "50px"),
    fill="#18FF00",
    font_size="36px",
    font_weight="bold"
)
# Glow filter
filter_glow = dwg.defs.add(dwg.filter(id="glow"))
filter_glow.feGaussianBlur(in_="SourceGraphic", stdDeviation=4, result="blur")
filter_glow.feMerge().feMergeNode(in_="blur")
filter_glow.feMerge().feMergeNode(in_="SourceGraphic")
title['filter'] = "url(#glow)"
dwg.add(title)

# Top MITRE Techniques
techniques = [
    "TA0001 Initial Access",
    "TA0002 Execution",
    "TA0003 Persistence",
    "TA0004 Privilege Escalation",
    "TA0005 Defense Evasion"
]

y_start = 120
dwg.add(dwg.text("Top Techniques:", insert=("40px", y_start - 20), fill="#18FF00", font_size="24px"))
for i, t in enumerate(techniques):
    text = dwg.text(t, insert=("60px", f"{y_start + i*40}px"), fill="white", font_size="20px")
    dwg.add(text)
    # Color pulse animation
    text.add(dwg.animate(attributeName="fill", values="white;#18FF00;white", dur=f"{1.5 + i*0.3}s", repeatCount="indefinite"))

# Alerts / Incidents
alerts = {
    "Critical Alerts": 12,
    "High Alerts": 34,
    "Medium Alerts": 56
}
y_alerts = 120
dwg.add(dwg.text("Current Alerts:", insert=("500px", y_alerts - 20), fill="#18FF00", font_size="24px"))
for i, (k, v) in enumerate(alerts.items()):
    text = dwg.text(f"{k}: {v}", insert=("520px", f"{y_alerts + i*40}px"), fill="white", font_size="20px")
    dwg.add(text)
    # Counter glow animation
    text.add(dwg.animate(attributeName="fill", values="white;#FF0000;white", dur=f"{2 + i*0.3}s", repeatCount="indefinite"))

# Top Threat Actors
actors = ["APT1", "APT29", "FIN7", "Lazarus Group", "Magecart"]
y_actors = 300
dwg.add(dwg.text("Top Threat Actors:", insert=("40px", y_actors - 20), fill="#18FF00", font_size="24px"))
for i, a in enumerate(actors):
    text = dwg.text(a, insert=("60px", f"{y_actors + i*40}px"), fill="white", font_size="20px")
    dwg.add(text)
    text.add(dwg.animate(attributeName="fill", values="white;#FF00FF;white", dur=f"{1.8 + i*0.3}s", repeatCount="indefinite"))

# Recent Events / Logs
events = [
    "User login failed - 12:34",
    "Malware detected - 12:40",
    "Suspicious process - 12:45",
    "Privilege escalation attempt - 12:50",
    "Phishing email blocked - 12:55"
]
y_events = 300
dwg.add(dwg.text("Recent Events:", insert=("500px", y_events - 20), fill="#18FF00", font_size="24px"))
for i, e in enumerate(events):
    text = dwg.text(e, insert=("520px", f"{y_events + i*40}px"), fill="white", font_size="18px")
    dwg.add(text)
    text.add(dwg.animate(attributeName="fill", values="white;#00FFFF;white", dur=f"{2.2 + i*0.3}s", repeatCount="indefinite"))

dwg.save()

