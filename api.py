from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

STAFF_CACHE = []

@app.route("/")
def home():
    return "API GENNOVERA RUNNING"

@app.route("/staff", methods=["POST"])
def staff():
    global STAFF_CACHE
    data = request.json
    STAFF_CACHE = data.get("data", [])

    print("📦 STAFF UPDATED:", len(STAFF_CACHE))
    return jsonify({"status": "ok", "count": len(STAFF_CACHE)})

@app.route("/staff", methods=["GET"])
def get_staff():
    return jsonify(STAFF_CACHE)

# 🔥 IMPORTANT untuk Railway
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)