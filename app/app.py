import os
import threading
import time

from flask import Flask, jsonify, render_template

app = Flask(__name__)

START_TIME = time.time()
state = {"healthy": True}  # in-memory flag; resets whenever the container restarts


@app.route("/")
def home():
    return render_template("index.html", healthy=state["healthy"])


@app.route("/health")
def health():
    """Used by Docker health checks. Returns 200 if OK, 503 if broken."""
    if state["healthy"]:
        return jsonify(status="healthy", uptime_seconds=round(time.time() - START_TIME, 1)), 200
    return jsonify(status="unhealthy"), 503


@app.route("/break", methods=["POST"])
def break_app():
    """Failure simulation #1: app stays running but reports unhealthy."""
    state["healthy"] = False
    return jsonify(message="App is now unhealthy. Autoheal should restart it soon."), 200


@app.route("/crash", methods=["POST"])
def crash():
    """Failure simulation #2: kill the process so the container exits."""
    threading.Timer(0.5, lambda: os._exit(1)).start()
    return jsonify(message="Crashing in 0.5 seconds..."), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
