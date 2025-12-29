import json

nodes = [
    {"name": "HostA", "x": 300, "y": 100, "color": "#ff4e4e"},
    {"name": "Server42", "x": 450, "y": 200, "color": "#4effff"}
]

svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400">'
svg_content += '<rect width="600" height="400" fill="#0a0f1a"/>'

for node in nodes:
    svg_content += f'''
    <circle cx="{node["x"]}" cy="{node["y"]}" r="6" fill="{node["color"]}">
        <animate attributeName="r" values="6;10;6" dur="3s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite"/>
    </circle>
    <text x="{node["x"]+10}" y="{node["y"]+5}" font-family="Consolas, monospace" font-size="12" fill="#a0c8ff">{node["name"]}</text>
    '''

svg_content += '</svg>'

with open("assets/globe_live.svg", "w") as f:
    f.write(svg_content)

print("SVG generated successfully!")

