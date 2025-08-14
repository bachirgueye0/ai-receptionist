from flask import Flask, request, Response
from twilio.request_validator import RequestValidator
import os

# ENV VARS set in Render
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")  # ok to leave blank for now
STREAM_WSS = os.environ.get("STREAM_WSS", "wss://placeholder.com/twilio-stream")
COMPANY_NAME = os.environ.get("COMPANY_NAME", "Your Company")

app = Flask(__name__)
validator = RequestValidator(TWILIO_AUTH_TOKEN) if TWILIO_AUTH_TOKEN else None

def validate(req):
    if not validator:
        return True  # dev mode: skip signature check
    signature = request.headers.get("X-Twilio-Signature", "")
    url = request.url
    params = request.form.to_dict()
    return validator.validate(url, params, signature)

# Allow GET (for quick browser test) and POST (what Twilio uses)
@app.route("/voice", methods=["GET", "POST"])
def voice():
    if request.method == "POST" and not validate(request):
        return "invalid signature", 403

    resp = f"""
<Response>
  <Say>Thanks for calling {COMPANY_NAME}. Connecting you now.</Say>
  <Connect>
    <Stream url="{STREAM_WSS}"/>
  </Connect>
</Response>"""
    return Response(resp.strip(), mimetype="text/xml")

@app.get("/")
def root():
    return "AI receptionist entry is running. Use /voice (POST) for Twilio."
