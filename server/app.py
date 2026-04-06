from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# In-memory storage
otp_store = {}
ride = {
    "status": "idle",
    "user": None,
    "driver": "Driver1",
    "price": 0,
    "rating": None
}

# Generate OTP
@app.route('/send-otp', methods=['POST'])
def send_otp():
    phone = request.json['phone']
    otp = str(random.randint(1000, 9999))
    otp_store[phone] = otp
    print("OTP:", otp)  # show in terminal
    return jsonify({"message": "OTP sent"})

# Verify OTP
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    phone = request.json['phone']
    otp = request.json['otp']
    
    if otp_store.get(phone) == otp:
        return jsonify({"status": "verified"})
    return jsonify({"status": "failed"})

# Book Ride
@app.route('/book', methods=['POST'])
def book():
    ride["status"] = "requested"
    ride["user"] = request.json['user']
    ride["price"] = random.randint(100, 300)
    
    return jsonify({
        "message": "Ride booked",
        "price": ride["price"]
    })

# Driver checks ride
@app.route('/driver/status')
def driver_status():
    return jsonify(ride)

# Driver accepts
@app.route('/driver/accept', methods=['POST'])
def accept():
    ride["status"] = "accepted"
    return jsonify({"message": "Ride accepted"})

# Complete ride
@app.route('/complete', methods=['POST'])
def complete():
    ride["status"] = "completed"
    return jsonify({"message": "Ride completed"})

# Rating
@app.route('/rate', methods=['POST'])
def rate():
    ride["rating"] = request.json['rating']
    return jsonify({"message": "Thanks for rating!"})

app.run(host="0.0.0.0", port=5000, debug=True)