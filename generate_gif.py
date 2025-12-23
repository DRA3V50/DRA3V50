from PIL import Image, ImageDraw
import subprocess, math

# Radar settings
SIZE = 520
CENTER = SIZE // 2
RADIUS = 220
BG = (5, 15, 30)          # Dark SOC blue
RADAR = (0, 200, 255)     # Cyan sweep
BLIP = (0, 255, 200)      # Activity blip color

# Map domains to angles
DOMAINS = {
    "soc": 0,
    "ir": 60,
    "siem": 120,
    "soar": 180,
    "edr": 240,
    "data": 300
}

# Keywords to detect commits related to each domain
KEYWORDS = {
    "soc": ["soc", "ticket", "monitor", "helpdesk"],
    "ir": ["incident", "alert", "response", "investigation"],
    "siem": ["splunk", "sentinel", "log", "siem", "rules"],
    "soar": ["automation", "playbook", "workflow", "soar"],
    "edr": ["crowdstrike", "defender", "edr", "endpoint"],
    "data": ["data", "analytics", "report", "dashboard"]
}

def get_activity():
    # Get commit messages and changed file paths
    log = subprocess.check_output(
        ["git", "log", "--name-only", "--pretty=format:%s"], text=True
    )

    activity = {k: 0 for k in DOMAINS}

    for line in log.splitlines():
        line_lower = line.lower()
        for domain, keywords in KEYWORDS.items():
            if any(k in line_lower for k in keywords):
                activity[domain] += 1

    return activity

activity = get_activity()
frames = []

for sweep in range(0, 360, 5):
    img = Image.new("RGB", (SIZE, SIZE), BG)
    d = ImageDraw.Draw(img)

    # Outer radar circle
    d.ellipse(
        (CENTER-RADIUS, CENTER-RADIUS, CENTER+RADIUS, CENTER+RADIUS),
        outline=RADAR, width=2
    )

    # Sweep line
    angle = math.radians(sweep)
    sx = CENTER + RADIUS * math.cos(angle)
    sy = CENTER + RADIUS * math.sin(angle)
    d.line((CENTER, CENTER, sx, sy), fill=RADAR, width=2)

    # Draw blips
    for domain, base_angle in DOMAINS.items():
        count = activity[domain]
        for i in range(count):
            r = 40 + i * 12  # distance from center
            a = math.radians(base_angle)
            x = CENTER + r * math.cos(a)
            y = CENTER + r * math.sin(a)
            d.ellipse((x-3, y-3, x+3, y+3), fill=BLIP)

    frames.append(img)

# Save animated GIF
frames[0].save(
    "generated.gif",
    save_all=True,
    append_images=frames[1:],
    duration=80,
    loop=0
)
