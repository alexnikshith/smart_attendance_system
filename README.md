# 📌 Smart Attendance System using QR Code

A web-based **Smart Attendance Management System** built using **Flask (Python)** and **SQLite**, where faculty can generate QR codes for each class session and students can scan the QR code to mark attendance securely.

---

## 🚀 Features

### 👨‍🏫 Faculty
- Login & dashboard
- Generate **unique QR code** for every class session
- View attendance records of students
- Prevents duplicate attendance for the same session

### 👨‍🎓 Student
- Login & dashboard
- Scan QR code to mark attendance
- View total classes attended
- View attendance percentage (capped at 100%)

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **QR Code:** `qrcode` Python library
- **Session Management:** Flask Sessions

---

## 📂 Project Structure
smart_attendance_system/
│
├── app.py
├── database/
│ └── attendance.db
│
├── templates/
│ ├── login.html
│ ├── register.html
│ ├── student_dashboard.html
│ ├── faculty_dashboard.html
│ ├── scan_qr.html
│ ├── attendance_percentage.html
│ ├── attendance_success.html
│ ├── attendance_exists.html
│ └── view_attendance.html
│
├── static/
│ └── css/
│ └── style.css
│
├── utils/
│ └── qr_generator.py
│
└── README.md

