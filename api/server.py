from flask import Flask, jsonify, send_from_directory
import psutil
import platform
import socket
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "public"

app = Flask(__name__, static_folder=str(STATIC_DIR))


def get_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "127.0.0.1"

@app.route('/api/stats')
def stats():
    disk = psutil.disk_usage('/')
    mem = psutil.virtual_memory()

    return jsonify({
        "hostname": platform.node(),
        "os": platform.system(),
        "ip": get_ip(),
        "cpu": psutil.cpu_percent(interval=0.4),
        "memory": mem.percent,
        "disk": disk.percent,
        "cores": psutil.cpu_count(),
        "network_sent": round(psutil.net_io_counters().bytes_sent / (1024*1024), 2),
        "network_recv": round(psutil.net_io_counters().bytes_recv / (1024*1024), 2)
    })

@app.route('/')
def index():
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(STATIC_DIR, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
