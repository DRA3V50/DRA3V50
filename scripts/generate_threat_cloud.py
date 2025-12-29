import random
import os

os.makedirs("assets", exist_ok=True)

WIDTH = 250
HEIGHT = 150

# Threats
threats = [
    {"name": "Ransomware", "color": "#ff4e4e"},
    {"name": "Phishing", "color": "#ffb74e"},
    {"name": "Vulnerability", "color": "#4effff"}
]

# Randomize number of particles
for t in threats:
    t["count"] = random.randint(5, 12)

with open("assets/live_threat_cloud.svg", "w") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}">\n')
    f.write(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#0a0f1a"/>\n')

    particle_id = 0
    for t in threats:
        for _ in range(t["count"]):
            x = random.randint(20, WIDTH-20)
            y = random.randint(20, HEIGHT-20)
            f.write(f'<circle id="p{particle_id}" cx="{x}" cy="{y}" r="4" fill="{t["color"]}">\n')
            f.write('<animate attributeName="r" values="2;6;2" dur="2s" repeatCount="indefinite"/>\n')
            f.write('<animate attributeName="cx" values="{x};{x_plus};{x}" dur="3s" repeatCount="indefinite"/>\n'.format(
                x=x, x_plus=x+random.randint(-10,10)))
            f.write('<animate attributeName="cy" values="{y};{y_plus};{y}" dur="3s" repeatCount="indefinite"/>\n'.format(
                y=y, y_plus=y+random.randint(-10,10)))
            f.write('</circle>\n')
            particle_id += 1

    f.write('</svg>\n')

print("Live Threat Cloud SVG generated!")

