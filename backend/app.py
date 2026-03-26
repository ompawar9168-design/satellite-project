from flask import Flask, jsonify
from flask_cors import CORS
from routes.analysis_routes import analysis_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(analysis_bp, url_prefix="/api")


@app.route("/")
def home():
    return "Satellite Backend Running 🚀"


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Backend is running"
    })


@app.route("/api/test", methods=["GET"])
def test_api():
    return jsonify({
        "status": "success",
        "message": "Backend Connected Successfully"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)