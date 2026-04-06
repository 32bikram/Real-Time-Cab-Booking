from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

ride_data = {
    "requested": False,
    "accepted": False,
    "otp": None,
    "verified": False,
    "completed": False,
    "fare": 0,
    "paid": False
}

# ---------------- ROUTES ----------------

@app.route("/")
def login():
    return render_template("client_login.html")


@app.route("/dashboard", methods=["POST"])
def dashboard():
    return render_template("client_dashboard.html")


@app.route("/ride")
def ride():
    return render_template("client_ride.html")


@app.route("/payment")
def payment():
    fare = request.args.get("fare")
    return render_template("client_payment.html", fare=fare)


@app.route("/driver")
def driver():
    return render_template("driver.html")


# ---------------- SOCKET EVENTS ----------------

@socketio.on("connect")
def connect():
    print("🔌 Client connected")


@socketio.on("book_ride")
def book_ride(data):
    print("🚕 Ride requested:", data)

    ride_data["requested"] = True

    emit("new_request", data, broadcast=True)


@socketio.on("accept_ride")
def accept_ride():
    print("✅ Driver accepted ride")

    ride_data["accepted"] = True
    ride_data["otp"] = random.randint(1000, 9999)

    emit("ride_accepted", {"otp": ride_data["otp"]}, broadcast=True)


@socketio.on("verify_otp")
def verify_otp(data):
    if str(data["otp"]) == str(ride_data["otp"]):
        print("🔓 OTP Verified")

        ride_data["verified"] = True
        emit("otp_success", broadcast=True)
    else:
        emit("otp_failed")


@socketio.on("complete_ride")
def complete_ride():
    ride_data["completed"] = True
    ride_data["fare"] = random.randint(100, 500)

    print(f"💰 Fare: ₹{ride_data['fare']}")

    emit("ride_completed", {"fare": ride_data["fare"]}, broadcast=True)


@socketio.on("make_payment")
def make_payment(data):
    if int(data["amount"]) == ride_data["fare"]:
        print("📩 SMS: Payment received")

        emit("payment_success", broadcast=True)
    else:
        emit("payment_failed")


# ---------------- RUN ----------------

if __name__ == "__main__":
    socketio.run(app, debug=True)