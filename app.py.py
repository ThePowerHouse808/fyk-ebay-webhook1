import os
from flask import Flask, request, Response

app = Flask(__name__)

# Replace this value later with your eBay token
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN", "FYK123TOKEN")

@app.route("/", methods=["GET"])
def root():
    return Response("OK", status=200, mimetype="text/plain")

@app.route("/ebay/delete", methods=["GET", "POST"])
def ebay_delete():
    if request.method == "GET":
        return Response(VERIFICATION_TOKEN, status=200, mimetype="text/plain")
    _ = request.get_json(silent=True)
    return Response("OK", status=200, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
