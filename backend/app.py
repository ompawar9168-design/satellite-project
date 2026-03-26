from flask import Flask, jsonify
from flask_cors import CORS
from routes.analysis_routes import analysis_bp

app = Flask(__name__)
CORS(app)

# Register routes
app.register_blueprint(analysis_bp, url_prefix="/api")

# ✅ HEALTH ROUTE (IMPORTANT)
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Backend is running"
    })

# Optional test route
@app.route("/")
def home():
    return "Backend Running 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)