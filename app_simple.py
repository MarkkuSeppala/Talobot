from flask import Flask, request, render_template, Response, jsonify
import os
import logging

# Yksinkertainen logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "OK", "message": "Sovellus toimii"})

@app.route("/test")
def test():
    return "Test-sivu toimii!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting simplified app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
