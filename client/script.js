const SERVER = "http://localhost:5000";

async function sendOTP() {
    const phone = document.getElementById("phone").value;

    await fetch(`${SERVER}/send-otp`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({phone})
    });

    alert("OTP sent (check server terminal)");
}

async function verifyOTP() {
    const phone = document.getElementById("phone").value;
    const otp = document.getElementById("otp").value;

    const res = await fetch(`${SERVER}/verify-otp`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({phone, otp})
    });

    const data = await res.json();
    document.getElementById("status").innerText = "Status: " + data.status;
}

async function bookRide() {
    const res = await fetch(`${SERVER}/book`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({user: "Bikram"})
    });

    const data = await res.json();

    document.getElementById("price").innerText =
        "💰 Price: ₹" + data.price;

    document.getElementById("status").innerText =
        "⏳ Waiting for driver...";

    startTrackingDriver();
}

// 🔥 NEW: Track driver status
function startTrackingDriver() {
    const interval = setInterval(async () => {
        const res = await fetch(`${SERVER}/driver/status`);
        const data = await res.json();

        if (data.status === "accepted") {
            document.getElementById("driver").innerText =
                "🚗 Driver Assigned: " + data.driver;

            document.getElementById("status").innerText =
                "Driver is on the way!";
        }

        if (data.status === "completed") {
            document.getElementById("status").innerText =
                "✅ Ride Completed";

            clearInterval(interval);
        }

    }, 2000); // every 2 sec
}

async function rateRide() {
    const rating = document.getElementById("rating").value;

    await fetch(`${SERVER}/rate`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({rating})
    });

    alert("Thanks for rating!");
}