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
BIO_CACHE = {}
BIO_FILE = "bio.json"


def load_bio():
    global BIO_CACHE

    if not os.path.exists(BIO_FILE):
        BIO_CACHE = {}
        return BIO_CACHE

    try:
        with open(BIO_FILE, "r", encoding="utf-8") as f:
            BIO_CACHE = json.load(f)
            return BIO_CACHE
    except:
        BIO_CACHE = {}
        return BIO_CACHE


def save_bio():
    global BIO_CACHE

    tmp = BIO_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(BIO_CACHE, f, indent=2)

    os.replace(tmp, BIO_FILE)


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
    load_bio()

    result = []

    for user in STAFF_CACHE:
        uid = str(user.get("id"))

        user["bio"] = BIO_CACHE.get(uid, {}).get("bio", "No bio available")
        result.append(user)

    return jsonify(result)

# =========================
# 🔥 GET ALL BIO LIST (INI YANG KAMU MAU)
# =========================
@app.route("/bio", methods=["GET"])
def get_all_bio():
    load_bio()

    result = [
        {
            "id": uid,
            "bio": data.get("bio", "")
        }
        for uid, data in BIO_CACHE.items()
    ]

    return jsonify({
        "count": len(result),
        "data": result
    })

# =========================
# GET SINGLE BIO
# =========================
@app.route("/bio/<user_id>", methods=["GET"])
def get_bio(user_id):
    load_bio()

    return jsonify({
        "id": user_id,
        "bio": BIO_CACHE.get(user_id, {}).get("bio", "")
    })


# =========================
# SET BIO
# =========================
@app.route("/bio/set", methods=["POST"])
def set_bio():
    load_bio()  # pastikan cache sync

    data = request.json
    user_id = str(data["id"])
    bio = data["bio"]

    if user_id not in BIO_CACHE:
        BIO_CACHE[user_id] = {}

    BIO_CACHE[user_id]["bio"] = bio

    save_bio()

    return jsonify({"status": "ok"})

# =========================
# ROLE CACHE
# =========================
ROLE_CACHE = []


# =========================
# ROLE UPDATE FROM BOT
# =========================
@app.route("/roles", methods=["POST"])
def update_roles():
    global ROLE_CACHE

    data = request.json

    ROLE_CACHE = data.get("data", [])

    print("🎭 ROLES UPDATED:", len(ROLE_CACHE))

    return jsonify({
        "status": "ok",
        "count": len(ROLE_CACHE)
    })


# =========================
# GET ALL ROLES
# =========================
@app.route("/roles", methods=["GET"])
def get_roles():

    return jsonify({
        "count": len(ROLE_CACHE),
        "data": ROLE_CACHE
    })


# =========================
# GET SINGLE ROLE
# =========================
@app.route("/roles/<role_id>", methods=["GET"])
def get_role(role_id):

    role = next(
        (
            r for r in ROLE_CACHE
            if str(r.get("id")) == str(role_id)
        ),
        None
    )

    if not role:
        return jsonify({
            "error": "Role not found"
        }), 404

    return jsonify(role)

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
