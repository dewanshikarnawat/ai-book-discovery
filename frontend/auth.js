
async function register() {
    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;

    if (!email || !password) {
        alert("Email and password required");
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:5000/register", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (res.ok || res.status === 200) {
            alert(data.message); // "OTP sent" ya "OTP resent"
            localStorage.setItem("pendingEmail", email);

            // OTP verification page ka path check karo
            window.location.href = "verifyOTP.html";
        } else {
            alert(data.error);
        }
    } catch (err) {
        console.error(err);
        alert("Server error");
    }
}



async function verifyOtp() {
    const email = localStorage.getItem("pendingEmail");
    const otp = document.getElementById("otpInput").value;

    const res = await fetch("http://127.0.0.1:5000/verify-otp", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email, otp })
    });

    const data = await res.json();
    if (res.ok) {
        alert("Email verified! Please login.");
        window.location.href = "login.html";
    } else {
        alert(data.error);
    }
}


// Login
async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    const res = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });

    const data = await res.json();
    if (res.ok) {
        localStorage.setItem("currentUser", data.user.email); // use localStorage
        window.location.href = "app.html";
    } else {
        document.getElementById('loginError').textContent = data.error;
    }
}

document.addEventListener("DOMContentLoaded", () => {

    // 🔐 Protect app.html
    if (window.location.pathname.endsWith("app.html")) {
        if (!localStorage.getItem("currentUser")) {
            window.location.href = "login.html";
            return;
        }

        const userGreeting = document.getElementById("userGreeting");
        if (userGreeting) {
            userGreeting.textContent = `👋 ${localStorage.getItem("currentUser")}`;
        }
    }

    // 🚪 Logout
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            console.log("✅ Logout clicked");
            localStorage.removeItem("currentUser");
            window.location.href = "login.html";
        });
    }
});