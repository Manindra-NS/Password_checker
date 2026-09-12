
import logging
import os
import sys
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

try:
    from flask import Flask, jsonify, request, send_from_directory
    from flask_cors import CORS
except ModuleNotFoundError as exc:
    logger.critical(
        "Missing dependency: %s\n"
        "Install everything with:  pip install -r requirements.txt",
        exc,
    )
    sys.exit(1)

from analyzer        import analyze_password
from breach_checker  import check_breach_flag
from entropy         import calculate_entropy
from pattern_detector import (
    common_password_checker,
    is_weak_password,
    load_common_passwords,
)


BASE_DIR = Path(__file__).resolve().parent   
app = Flask(
    __name__,
    static_folder=str(BASE_DIR),
    static_url_path="",
)


_cors_origins = os.environ.get("CORS_ORIGINS", "*")
CORS(app, resources={r"/api/*": {"origins": _cors_origins}})

MAX_PASSWORD_LEN = int(os.environ.get("MAX_PASSWORD_LEN", 512))

_common_pw_path = BASE_DIR / "common_passwords.txt"
try:
    COMMON_PASSWORDS: set = load_common_passwords(str(_common_pw_path))
    logger.info("Loaded %d common passwords from %s", len(COMMON_PASSWORDS), _common_pw_path)
except FileNotFoundError:
    logger.warning(
        "common_passwords.txt not found at %s — common-password check disabled.",
        _common_pw_path,
    )
    COMMON_PASSWORDS = set()


@app.before_request
def _start_timer():
    request._start_time = time.perf_counter()  


@app.after_request
def _log_request(response):
    elapsed_ms = (time.perf_counter() - request._start_time) * 1000  
    logger.info(
        "%s %s → %d  (%.1f ms)",
        request.method,
        request.path,
        response.status_code,
        elapsed_ms,
    )
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"]        = "DENY"
    response.headers["Referrer-Policy"]        = "strict-origin-when-cross-origin"
    return response



@app.route("/")
def index():
    """Serve the frontend SPA."""
    return send_from_directory(str(BASE_DIR), "index.html")


@app.route("/api/check-password", methods=["POST"])
def check_password():

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    password = data.get("password")
    if password is None:
        return jsonify({"error": "Missing field: 'password'"}), 400
    if not isinstance(password, str):
        return jsonify({"error": "'password' must be a string"}), 400
    if len(password) == 0:
        return jsonify({"error": "'password' must not be empty"}), 400
    if len(password) > MAX_PASSWORD_LEN:
        return jsonify({"error": f"'password' must be ≤ {MAX_PASSWORD_LEN} characters"}), 400

  
    analysis      = analyze_password(password)
    entropy_bits  = calculate_entropy(password)
    is_common     = common_password_checker(password, COMMON_PASSWORDS)

    
    breached = check_breach_flag(password)

   
    return jsonify({
        "checks": {
            "uppercase": analysis["hasUpper"],
            "lowercase": analysis["hasLower"],
            "digit":     analysis["hasDigit"],
            "special":   analysis["hasSpecial"],
        },
        "score": {
            "points": analysis["points"],
            "label":  analysis["label"],
        },
        "entropy":  round(entropy_bits, 1),
        "length":   analysis["length"],
        "common":   is_common,
        "breached": breached,
    })




@app.errorhandler(404)
def not_found(err):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(405)
def method_not_allowed(err):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(err):
    logger.exception("Unhandled server error")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "true").lower() in ("1", "true", "yes")
    logger.info("Starting dev server on http://127.0.0.1:%d  (debug=%s)", port, debug)
    app.run(debug=debug, host="0.0.0.0", port=port)