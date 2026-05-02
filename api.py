from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# =========================
# MEMORY CACHE STAFF
# =========================
STAFF_CACHE = []

# =========================
# BIO FILE
# =========================
BIO_FILE = "bio.json"


def load_bio():
    if not os.path.exists(BIO_FILE):
        return {}
    try:
        with open(BIO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_bio(data):
    with open(BIO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return "API GENNOVERA RUNNING"


# =========================
# STAFF UPDATE FROM BOT
# =========================
@app.route("/staff", methods=["POST"])
def staff():
    global STAFF_CACHE
    data = request.json

    STAFF_CACHE = data.get("data", [])

    print("📦 STAFF UPDATED:", len(STAFF_CACHE))
    return jsonify({"status": "ok", "count": len(STAFF_CACHE)})


# =========================
# GET STAFF + BIO MERGE
# =========================
@app.route("/staff", methods=["GET"])
def get_staff():
    bio_data = load_bio()
    result = []

    for user in STAFF_CACHE:
        uid = str(user.get("id"))

        user["bio"] = bio_data.get(uid, {}).get("bio", "No bio available")
        result.append(user)

    return jsonify(result)


# =========================
# 🔥 GET ALL BIO LIST (INI YANG KAMU MAU)
# =========================
@app.route("/bio", methods=["GET"])
def get_all_bio():
    bio_data = load_bio()

    result = []

    for user_id, data in bio_data.items():
        result.append({
            "id": user_id,
            "bio": data.get("bio", "")
        })

    return jsonify({
        "count": len(result),
        "data": result
    })


# =========================
# GET SINGLE BIO
# =========================
@app.route("/bio/<user_id>", methods=["GET"])
def get_bio(user_id):
    bio_data = load_bio()

    return jsonify({
        "id": user_id,
        "bio": bio_data.get(user_id, {}).get("bio", "")
    })


# =========================
# SET BIO
# =========================
@app.route("/bio/set", methods=["POST"])
def set_bio():
    bio_data = load_bio()

    data = request.json
    user_id = str(data["id"])
    bio = data["bio"]

    if user_id not in bio_data:
        bio_data[user_id] = {}

    bio_data[user_id]["bio"] = bio

    save_bio(bio_data)

    return jsonify({"status": "ok"})


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
