import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os

# --- Paths ---
DATA_FILE = "scripts/data.json"
OUTPUT_PNG = "assets/intel_dashboard.png"

# Ensure assets folder exists
os.makedirs(os.path.dirname(OUTPUT_PNG), exist_ok=True)

# --- Lane definitions ---
lanes = [
    {"name": "SOC", "color": (0, 255, 255)},                 # Cyan
    {"name": "IR", "color": (255, 165, 0)},                 # Orange
    {"name": "SIEM", "color": (30, 144, 255)},              # Dodger Blue
    {"name": "SOAR", "color": (153, 50, 204)},              # Dark Orchid
    {"name": "EDR", "color": (50, 205, 50)},                # Lime Green
    {"name": "Data Automation", "color": (255, 105, 180)},  # Hot Pink
    {"name": "Data Analysis & Intelligence", "color": (255, 255, 0)}  # Yellow
]

# Image size
IMG_WIDTH = 1000
IMG_HEIGHT = 600
LANE_WIDTH = IMG_WIDTH // len(lanes)
BORDER = 50
BLIP_SPACING = 50

# --- Load JSON data ---
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {lane["name"]: 3 for lane in lanes}

# --- Create image ---
img = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), "#0a0a23")
draw = ImageDraw.Draw(img)

# Font
try:
    font = ImageFont.truetype("arial.ttf", 16)
except:
    font = ImageFont.load_default()

# --- Draw lanes and blips ---
for idx, lane in enumerate(lanes):
    x0 = idx * LANE_WIDTH
    # Lane background
    draw.rectangle([x0, 0, x0 + LANE_WIDTH, IMG_HEIGHT], fill=(16,16,64))
    # Lane icon circle
    draw.ellipse([x0 + 10, 10, x0 + 30, 30], fill=lane["color"])
    # Lane title
    draw.text((x0 + 40, 10), lane["name"], fill=lane["color"], font=font)
    
    # Blips
    count = data.get(lane["name"], 0)
    for i in range(count):
        blip_x = x0 + LANE_WIDTH // 2 - 15
        blip_y = BORDER + i * BLIP_SPACING
        draw.ellipse([blip_x, blip_y, blip_x + 30, blip_y + 30], fill=lane["color"])

# --- Timestamp ---
now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
bbox = draw.textbbox((0,0), f"Last update: {now}", font=font)
w = bbox[2] - bbox[0]
h = bbox[3] - bbox[1]
draw.text(((IMG_WIDTH - w)//2, IMG_HEIGHT - h - 10), f"Last update: {now}", fill=(180,180,180), font=font)

# --- Save PNG ---
img.save(OUTPUT_PNG)
print(f"Generated {OUTPUT_PNG}")
