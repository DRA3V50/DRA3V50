import datetime
import random

# MITRE tactics & techniques
tactics = [
    {"name": "Initial Access", "techniques": ["Phishing", "Drive-by Compromise", "Supply Chain Compromise"]},
    {"name": "Execution", "techniques": ["Command-Line Interface", "PowerShell", "Scheduled Task"]},
    {"name": "Persistence", "techniques": ["Registry Run Keys", "Service Registry Permissions", "Boot or Logon Autostart"]},
]

coverage = {tech: random.uniform(0.3,1.0) for t in tactics for tech in t["techniques"]}
events = [
    (datetime.datetime.now() - datetime.timedelta(hours=5), "Initial Access", "Detected phishing campaign"),
    (datetime.datetime.now() - datetime.timedelta(hours=2), "Execution", "Suspicious PowerShell script"),
    (datetime.datetime.now() - datetime.timedelta(minutes=30), "Persistence", "New autorun key detected"),
]

svg_width = 700
svg_height = 400
cell_width = 200
cell_height = 50
start_x = 50
start_y = 50

def generate_technique_cell(x, y, coverage_score, name):
    red = int(255 * (1 - coverage_score))
    green = int(255 * coverage_score)
    color = f"rgb({red},{green},0)"
    return f'''
    <rect x="{x}" y="{y}" width="{cell_width-10}" height="{cell_height-10}" fill="{color}" stroke="#333" stroke-width="1">
        <title>{name} (Coverage: {coverage_score:.2f})</title>
    </rect>
    <text x="{x+5}" y="{y+30}" fill="#fff" font-family="monospace" font-size="14">{name}</text>
    '''

def generate_svg():
    svg = f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg" style="background:#0b0f14">'
    y = start_y
    for tactic in tactics:
        x = start_x
        svg += f'<text x="{x-40}" y="{y+30}" fill="#00ffcc" font-family="monospace" font-size="16" font-weight="bold">{tactic["name"]}</text>'
        for tech in tactic["techniques"]:
            cov = coverage.get(tech, 0)
            svg += generate_technique_cell(x, y, cov, tech)
            x += cell_width
        y += cell_height

    # Timeline axis
    timeline_y = y + 50
    svg += f'<line x1="{start_x}" y1="{timeline_y}" x2="{svg_width - start_x}" y2="{timeline_y}" stroke="#00ffcc" stroke-width="2"/>'

    now = datetime.datetime.now()
    timeline_start = now - datetime.timedelta(hours=6)
    timeline_end = now
    timeline_length = svg_width - 2*start_x

    # Plot events
    for ts, tactic_name, desc in events:
        pos_ratio = (ts - timeline_start).total_seconds() / (timeline_end - timeline_start).total_seconds()
        x = start_x + pos_ratio * timeline_length
        colors = {"Initial Access": "#0077ff", "Execution": "#00cc44", "Persistence": "#ffaa00"}
        color = colors.get(tactic_name, "#888")
        svg += f'<circle cx="{x:.1f}" cy="{timeline_y}" r="10" fill="{color}"><title>{tactic_name}: {desc}</title></circle>'

    # Animated slider
    svg += f'<rect x="{start_x}" y="{timeline_y-15}" width="5" height="30" fill="#00ffcc"><animate attributeName="x" from="{start_x}" to="{svg_width - start_x}" dur="30s" repeatCount="indefinite"/></rect>'
    svg += f'<text x="{start_x}" y="{svg_height - 10}" fill="#00ffcc" font-family="monospace" font-size="12">Last Update: {now.isoformat()}Z</text>'
    svg += '</svg>'
    return svg

if __name__ == "__main__":
    import os
    os.makedirs("assets", exist_ok=True)
    with open("assets/mitre_dashboard.svg", "w", encoding="utf-8") as f:
        f.write(generate_svg())

