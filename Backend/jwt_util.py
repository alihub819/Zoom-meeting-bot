import jwt
import time
from config import API_KEY, API_SECRET

# Generate JWT for Zoom API authentication
def generate_zoom_jwt():
    payload = {
        "iss": API_KEY,
        "exp": time.time() + 3600  # Token valid for 1 hour
    }
    token = jwt.encode(payload, API_SECRET, algorithm="HS256")
    return token
