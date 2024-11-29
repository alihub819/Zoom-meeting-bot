# OAuth App Credentials
CLIENT_ID = ""  # Replace with your Client ID
CLIENT_SECRET = ""  # Replace with your Client Secret
REDIRECT_URI = "http://localhost:5000/zoom/callback"  # URL to handle Zoom's redirect after authorization

# Webhook Tokens for Validation
ZOOM_SECRET_TOKEN = ""  # Replace with your Secret Token from Zoom dashboard
VERIFICATION_TOKEN = ""  # Replace with your Verification Token from Zoom dashboard

# Zoom API Base URL
ZOOM_API_BASE_URL = "https://api.zoom.us/v2"

# Scopes Required for the App
# Ensure these are added when creating your Zoom app
ZOOM_SCOPES = [
    "meeting:read",               # Read meeting details
    "meeting:write",              # Create or update meetings
    "recording:read",             # Access and download recordings
    "user:read",                  # Access user information
]
