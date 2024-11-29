import requests
from flask import Flask, request, jsonify, redirect
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, ZOOM_SECRET_TOKEN

app = Flask(__name__)

# In-memory storage for access token
ACCESS_TOKEN = None

# Step 1: Authorization URL
@app.route("/")
def home():
    auth_url = (
        f"https://zoom.us/oauth/authorize?"
        f"response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)

# Step 2: Handle Redirect and Exchange Code for Token
@app.route("/zoom/callback")
def zoom_callback():
    global ACCESS_TOKEN

    auth_code = request.args.get("code")
    if not auth_code:
        return jsonify({"error": "Authorization code not provided"}), 400

    # Exchange the authorization code for an access token
    token_url = "https://zoom.us/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post(token_url, headers=headers, data=payload)

    if response.status_code == 200:
        token_data = response.json()
        ACCESS_TOKEN = token_data["access_token"]
        return jsonify({"access_token": ACCESS_TOKEN, "token_data": token_data}), 200
    else:
        return jsonify({"error": response.json()}), response.status_code

# Step 3: Fetch Meeting Recordings
@app.route("/fetch_recordings/<meeting_id>", methods=["GET"])
def fetch_recordings(meeting_id):
    global ACCESS_TOKEN
    if not ACCESS_TOKEN:
        return jsonify({"error": "Access token not available. Please authenticate first."}), 401

    url = f"https://api.zoom.us/v2/meetings/{meeting_id}/recordings"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": response.json()}), response.status_code

# Step 4: Webhook Validation
@app.route("/webhook", methods=["POST"])
def zoom_webhook():
    # Validate Secret Token
    received_token = request.headers.get("Authorization")
    if received_token != ZOOM_SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # Process webhook event
    data = request.json
    event = data.get("event")
    if event == "recording.completed":
        meeting_id = data["payload"]["object"]["id"]
        return jsonify({"message": f"Recording completed for meeting {meeting_id}"}), 200

    return jsonify({"message": "Event not handled"}), 200

if __name__ == "__main__":
    app.run(debug=True)
