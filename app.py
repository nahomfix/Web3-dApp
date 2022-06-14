from datetime import datetime

from flask import Flask, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def index():
    return make_response(
        jsonify({"timestamp": datetime.now().isoformat()}), 200
    )


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
