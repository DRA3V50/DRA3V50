import json
import random
from datetime import datetime
from flask import Flask, jsonify, send_from_directory
from pathlib import Path

app = Flask(__name__)
ASSETS_DIR = Path(__file__).parent.parent / "assets"

DATA_FILE = ASSETS_DIR / "dashboard_data.json"

# Ensure JSON exists
if not DATA_FILE.exists():
    DATA_FILE.write_text(json.dumps({
        "critical": 0,
        "abnormal": 0,
        "medium": 0,
        "investigated": 0,
        "updated": "-"
    }, indent=2))

@app.route("/metrics")
def metrics():
    """Return live metrics."""
    data = {
        "critical": random.randint(10, 40),
        "abnormal": random.randint(30, 80),
        "medium": random.randint(60, 120),
        "investigated": random.randint(100, 200),
        "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    # Save to JSON
    DATA_FILE.write_text(json.dumps(data, indent=2))
    return jsonify(data)

@app.route("/<path:filename>")
def assets(filename):
    """Serve assets folder files (HTML, SVG)."""
    return send_from_directory(ASSETS_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
