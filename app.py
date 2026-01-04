from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# -------------------------------
# 🔗 Register Your API Endpoints
# -------------------------------
SERVICE_APIS = {
    "phone": "https://source-code-api.vercel.app/?num=",
    "pan": "https://abbas-apis.vercel.app/api/pan?pan=",
    "vehicle": "https://Tobi-rc-api.vercel.app/?rc_number=",
    "ifsc": "https://abbas-apis.vercel.app/api/ifsc?ifsc=",
    "gmail": "https://abbas-apis.vercel.app/api/email?mail=",
    "instagram": "https://abbas-apis.vercel.app/api/instagram?username=",
    "ip": "https://abbas-apis.vercel.app/api/ip?ip=",
    "pak_number": "https://abbas-apis.vercel.app/api/pakistan?number=",
    "ff_uid": "https://abbas-apis.vercel.app/api/ff-info?uid=",
    "ff_ban": "https://abbas-apis.vercel.app/api/ff-ban?uid="
}

# -----------------------------------
# 🧹 extract only "data" / "details"
# -----------------------------------
def extract_useful_fields(response_json):
    if "details" in response_json:
        return response_json["details"]

    if "data" in response_json:
        return response_json["data"]

    return response_json


# ---------------------------
# ⚡ API Proxy Route
# ---------------------------
@app.route("/fetch", methods=["POST"])
def fetch_data():
    data = request.json
    service = data.get("service")
    query = data.get("query")

    if service not in SERVICE_APIS:
        return jsonify({"success": False, "message": "Invalid service"}), 400

    try:
        api_url = SERVICE_APIS[service] + query
        r = requests.get(api_url, timeout=15)
        r.raise_for_status()

        cleaned = extract_useful_fields(r.json())

        return jsonify({
            "success": True,
            "result": cleaned
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "No Data Found or API Error"
        })


# ---------------------------
# 🌐 Home Page
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    