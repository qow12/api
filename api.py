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
# BIO FILE (DISCORD INPUT)
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


# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return "API GENNOVERA RUNNING"


# =========================
# DISCORD BOT PUSH STAFF DATA
# =========================
@app.route("/staff", methods=["POST"])
def staff():
    global STAFF_CACHE
    data = request.json

    STAFF_CACHE = data.get("data", [])

    print("📦 STAFF UPDATED:", len(STAFF_CACHE))
    return jsonify({"status": "ok", "count": len(STAFF_CACHE)})


# =========================
# GET STAFF (FRONTEND)
# =========================
@app.route("/staff", methods=["GET"])
def get_staff():
    bio_data = load_bio()

    # merge staff + bio
    result = []

    for user in STAFF_CACHE:
        uid = str(user.get("id"))

        user["bio"] = bio_data.get(uid, {}).get("bio", "No bio available")

        result.append(user)

    return jsonify(result)


# =========================
# OPTIONAL: GET SINGLE BIO
# =========================
@app.route("/bio/<user_id>", methods=["GET"])
def get_bio(user_id):
    bio_data = load_bio()
    return jsonify({
        "bio": bio_data.get(user_id, {}).get("bio", "")
    })


# =========================
# OPTIONAL: UPDATE BIO (DISCORD BOT ONLY)
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

    with open(BIO_FILE, "w", encoding="utf-8") as f:
        json.dump(bio_data, f, indent=2)

    return jsonify({"status": "ok"})


# =========================
# RUN (RAILWAY SUPPORT)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
