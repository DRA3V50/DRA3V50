import json
import random
import time
from datetime import datetime
from pathlib import Path

# ----------------------
# CONFIG
# ----------------------
LIVE = False  # Set True for local live updates, False for GitHub Actions / CI
UPDATE_INTERVAL = 10  # seconds (only used if LIVE=True)

# Paths
ASSETS_DIR = Path("assets")
DATA_FILE = ASSETS_DIR / "dashboard_data.json"
SVG_FILE = ASSETS_DIR / "live_dashboard.svg"
HTML_FILE = ASSETS_DIR / "dashboard.html"

# Ensure assets folder exists
ASSETS_DIR.mkdir(exist_ok=True)

# ----------------------
# FUNCTIONS
# ----------------------
def generate_data():
    """Generate random live-ish data."""
    return {
        "critical": random.randint(10, 40),
        "abnormal": random.randint(30, 80),  # Using 'abnormal' instead of 'high severity'
        "medium": random.randint(60, 120),
        "investigated": random.randint(100, 200),
        "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

def save_json(data):
    """Save data to JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def build_svg(data):
    """Generate SVG dashboard with subtle animations."""
    svg = f"""
<svg width="300" height="180" xmlns="http://www.w3.org/2000/svg">
  <style>
    text {{ font-family: Arial, sans-serif; fill: #e5e7eb; }}
    .title {{ font-size: 16px; font-weight: bold; }}
    .metric {{ font-size: 18px; }}
    .critical {{ fill: #ef4444; }}
    .high {{ fill: #f97316; }}
    .medium {{ fill: #facc15; }}
    .ok {{ fill: #22c55e; }}
    .small {{ font-size: 12px; fill: #94a3b8; }}
  </style>

  <rect width="100%" height="100%" rx="12" fill="#0f172a"/>

  <text x="20" y="28" class="title">Threat Intelligence Dashboard</text>

  <text x="20" y="60" class="metric critical">
    Critical Alerts: {data.get("critical",0)}
    <animate attributeName="fill" values="#ef4444;#ff6666;#ef4444" dur="0.5s" begin="0s" repeatCount="1" />
  </text>
  <text x="20" y="90" class="metric high">
    Abnormal Alerts: {data.get("abnormal",0)}
    <animate attributeName="fill" values="#f97316;#ffae5c;#f97316" dur="0.5s" begin="0s" repeatCount="1" />
  </text>
  <text x="20" y="120" class="metric medium">
    Medium Severity: {data.get("medium",0)}
    <animate attributeName="fill" values="#facc15;#fff48f;#facc15" dur="0.5s" begin="0s" repeatCount="1" />
  </text>
  <text x="20" y="150" class="metric ok">
    Investigated: {data.get("investigated",0)}
    <animate attributeName="fill" values="#22c55e;#7fe77f;#22c55e" dur="0.5s" begin="0s" repeatCount="1" />
  </text>
  <text x="20" y="165" class="small">Updated: {data.get("updated","")}</text>
</svg>
"""
    with open(SVG_FILE, "w") as f:
        f.write(svg)

def build_html():
    """Generate HTML page that reloads the SVG every 5 seconds."""
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Live Threat Intelligence Dashboard</title>
<style>
  body {{
    background-color: #0f172a;
    color: #e5e7eb;
    font-family: Arial, sans-serif;
    display: flex;
    justify-content: center;
    padding: 20px;
  }}
  .dashboard {{
    width: 320px;
  }}
</style>
</head>
<body>
<div class="dashboard">
  <object id="dashboard-svg" type="image/svg+xml" data="{SVG_FILE.name}" width="100%" height="auto"></object>
</div>

<script>
  // Reload the SVG every 5 seconds to simulate live updates
  setInterval(() => {{
    const svgObject = document.getElementById('dashboard-svg');
    const timestamp = new Date().getTime(); // cache buster
    svgObject.data = "{SVG_FILE.name}?cb=" + timestamp;
  }}, 5000);
</script>
</body>
</html>
"""
    with open(HTML_FILE, "w") as f:
        f.write(html_content)

# ----------------------
# MAIN LOOP
# ----------------------
def main():
    if LIVE:
        print("Live dashboard running locally... press Ctrl+C to stop")
        try:
            while True:
                data = generate_data()
                save_json(data)
                build_svg(data)
                build_html()
                time.sleep(UPDATE_INTERVAL)
        except KeyboardInterrupt:
            print("\nStopped live dashboard.")
    else:
        # Single run (for GitHub Actions / CI)
        data = generate_data()
        save_json(data)
        build_svg(data)
        build_html()
        print("Dashboard updated successfully (single run)")

if __name__ == "__main__":
    main()

