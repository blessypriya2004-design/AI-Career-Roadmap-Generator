
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "frontend.html")

@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(".", filename)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "success": True,
        "message": "Career roadmap generator is running!",
        "roadmap": data
    })

if __name__ == "__main__":
    app.run()
