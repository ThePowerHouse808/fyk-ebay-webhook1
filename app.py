import os, hashlib, json
from flask import Flask, request, Response

app = Flask(__name__)

# Read from env (Render + local). Do NOT hardcode tokens here.
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN", "").strip()
ENDPOINT_URL = os.getenv("ENDPOINT_URL", "").strip()

def json_response(obj: dict, status=200):
    return Response(json.dumps(obj), status=status, mimetype="application/json")

@app.route("/", methods=["GET"])
def root():
    return Response("OK", status=200, mimetype="text/plain")

# Accept both paths and support GET/HEAD (challenge) + POST (notifications)
@app.route("/ebay/delete", methods=["GET", "POST", "HEAD"])
@app.route("/ebay/delete/", methods=["GET", "POST", "HEAD"])
def ebay_delete():
    if request.method in ("GET", "HEAD"):
        challenge_code = request.args.get("challenge_code", "")
        if challenge_code:
            # EXACT order: challengeCode + verificationToken + endpointURL
            payload = (challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL).encode("utf-8")
            digest = hashlib.sha256(payload).hexdigest()
            return json_response({"challengeResponse": digest})
        # Visiting without challenge just returns OK (NOT the token)
        return Response("OK", status=200, mimetype="text/plain")

    # POST = deletion notification (ack 200 OK)
    _ = request.get_json(silent=True)
    return Response("OK", status=200, mimetype="text/plain")

if __name__ == "__main__":
    # local run
    app.run(host="0.0.0.0", port=5000)
