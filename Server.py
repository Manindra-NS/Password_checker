from flask import Flask, request, jsonify
from flask_cors import CORS

from analyzer import analyze_password
from pattern_detector import isWeakPassword, loadCommonPasswords 
from entropy import calculate_entropy
from breach_checker import check_breach_flag

app = Flask(__name__)

CORS(app)

common_passwords = loadCommonPasswords()

@app.route("/")
def home():
    return "Python backend is working!"

@app.route("/check-password", methods=["POST"])
def check_password():

    data = request.get_json()

    password = data["password"]

    analysis = analyze_password(password)
    commonPassword = isWeakPassword(password,common_passwords)
    entropy = calculate_entropy(password)
    breached = check_breach_flag(password)
    
    print("Analysis:", analysis)

    return jsonify({
        "analysis": analysis,
        "commonPassword": commonPassword,
        "entropy": entropy,
        "breached": breached
    })
    

app.run(debug=False)