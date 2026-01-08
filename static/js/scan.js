// scan.js - Smart Attendance System

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const qrInput = document.querySelector("textarea");

    if (!form || !qrInput) return;

    form.addEventListener("submit", function (event) {
        // Prevent empty submission
        if (qrInput.value.trim() === "") {
            alert("Please paste QR code data before submitting.");
            event.preventDefault();
            return;
        }

        // Prevent duplicate attendance (basic client-side check)
        if (sessionStorage.getItem("attendance_marked")) {
            alert("Attendance already submitted for this session.");
            event.preventDefault();
            return;
        }

        // Mark attendance as submitted
        sessionStorage.setItem("attendance_marked", "true");
    });
});
