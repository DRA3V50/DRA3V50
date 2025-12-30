from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import random
import eventlet
eventlet.monkey_patch()  # for socketio with Flask

app = Flask(__name__)
socketio = SocketIO(app)

# Serve dashboard.html
@app.route('/')
def index():
    return send_from_directory('assets', 'dashboard.html')

# Function to generate live data
def generate_data():
    return {
        "critical": random.randint(10, 40),
        "abnormal": random.randint(30, 80),
        "medium": random.randint(60, 120),
        "investigated": random.randint(100, 200),
        "updated": socketio.server.manager.get_now().isoformat() if hasattr(socketio.server.manager, "get_now") else ""
    }

# Background task: emit updates every 5 seconds
def send_updates():
    while True:
        data = {
            "critical": random.randint(10, 40),
            "abnormal": random.randint(30, 80),
            "medium": random.randint(60, 120),
            "investigated": random.randint(100, 200),
            "updated": socketio.server.manager.get_now().isoformat() if hasattr(socketio.server.manager, "get_now") else ""
        }
        socketio.emit('update', data)
        socketio.sleep(5)

# Start background updates on server start
@socketio.on('connect')
def handle_connect():
    print("Client connected!")

# Start background thread
socketio.start_background_task(target=send_updates)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
