# from flask import Flask, render_template, request, redirect, session
# import sqlite3
# from utils.qr_generator import generate_qr
# from datetime import date
# from flask import request
# from datetime import datetime
# import json



# app = Flask(__name__)
# app.secret_key = "smart_attendance_secret"

# def get_db():
#     return sqlite3.connect("database/attendance.db")

# @app.route("/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]

#         conn = get_db()
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT id, role FROM users WHERE email=? AND password=?",
#             (email, password)
#         )
#         user = cursor.fetchone()
#         conn.close()

#         if user:
#             session["user_id"] = user[0]
#             session["role"] = user[1]

#             if user[1] == "student":
#                 return redirect("/student")
#             else:
#                 return redirect("/faculty")

#         return "<h3>Invalid Credentials</h3>"

#     return render_template("login.html")

# @app.route("/student")
# def student_dashboard():
#     if session.get("role") != "student":
#         return redirect("/")
#     return render_template("student_dashboard.html")


# @app.route("/faculty")
# def faculty_dashboard():
#     if session.get("role") != "faculty":
#         return redirect("/")
#     return render_template("faculty_dashboard.html")


# @app.route("/generate_qr")
# def generate_qr_route():
#     if session.get("role") != "faculty":
#         return redirect("/")

#     conn = get_db()
#     cursor = conn.cursor()

#     # Create a new session
#     cursor.execute("""
#         INSERT INTO sessions (faculty_id, subject, session_date, created_at)
#         VALUES (?, ?, ?, ?)
#     """, (
#         session["user_id"],
#         "Regular Class",
#         date.today().isoformat(),
#         datetime.now().isoformat()
#     ))

#     session_id = cursor.lastrowid
#     conn.commit()
#     conn.close()

#     generate_qr(session_id)

#     return render_template("faculty_dashboard.html", qr=True)


# @app.route("/scan_qr")
# def scan_qr():
#     if session.get("role") != "student":
#         return redirect("/")
#     return render_template("scan_qr.html")


# @app.route("/mark_attendance", methods=["POST"])
# def mark_attendance():
#     if session.get("role") != "student":
#         return redirect("/")

#     try:
#         qr_data = request.form["qrdata"]
#         data = json.loads(qr_data)
#         session_id = data["session_id"]
#     except:
#         return "❌ Invalid QR Code"

#     student_id = session["user_id"]

#     conn = get_db()
#     cursor = conn.cursor()

#     # Check if already marked for this session
#     cursor.execute("""
#         SELECT id FROM attendance
#         WHERE student_id = ? AND session_id = ?
#     """, (student_id, session_id))

#     if cursor.fetchone():
#         conn.close()
#         return render_template("attendance_exists.html")

#     # Mark attendance
#     cursor.execute("""
#         INSERT INTO attendance (student_id, session_id, status)
#         VALUES (?, ?, ?)
#     """, (student_id, session_id, "Present"))

#     conn.commit()
#     conn.close()

#     return render_template("attendance_success.html")


# @app.route("/attendance_percentage")
# def attendance_percentage():
#     student_id = session["user_id"]

#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT COUNT(DISTINCT session_id)
#         FROM attendance
#         WHERE student_id = ?
#     """, (student_id,))
#     attended = cursor.fetchone()[0]

#     cursor.execute("SELECT COUNT(*) FROM sessions")
#     total = cursor.fetchone()[0]

#     conn.close()

#     percentage = 0
#     if total > 0:
#         percentage = min((attended / total) * 100, 100)

#     # return render_template(
#     #     "attendance_percentage.html",
#     #     attended=attended,
#     #     total=total,
#     #     percentage=round(percentage, 2)
#     # )
#     return render_template("attendance_percentage.html",
#                            attended=attended,
#                            total=total,
#                            percentage=percentage)

# @app.route("/view_attendance")
# def view_attendance():
#     if session.get("role") != "faculty":
#         return redirect("/")

#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT users.name, attendance.date, attendance.status
#         FROM attendance
#         JOIN users ON users.id = attendance.student_id
#         ORDER BY attendance.date DESC
#     """)

#     records = cursor.fetchall()
#     conn.close()

#     return render_template("view_attendance.html", records=records)



# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         name = request.form["name"]
#         email = request.form["email"]
#         password = request.form["password"]
#         role = request.form["role"]

#         conn = get_db()
#         cursor = conn.cursor()

#         try:
#             cursor.execute(
#                 "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
#                 (name, email, password, role)
#             )
#             conn.commit()

#         except sqlite3.IntegrityError:
#             conn.close()
#             return """
#             <h3 style="color:red;">⚠ Email already registered</h3>
#             <a href="/register">Try another email</a>
#             """

#         finally:
#             conn.close()

#         return redirect("/")

#     return render_template("register.html")



# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect("/")

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=False)


from flask import Flask, render_template, request, redirect, session
import sqlite3
from utils.qr_generator import generate_qr
from datetime import date, datetime
import json

app = Flask(__name__)
app.secret_key = "smart_attendance_secret"


# =========================
# DATABASE CONNECTION
# =========================
def get_db():
    return sqlite3.connect("database/attendance.db")


# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, role FROM users WHERE email=? AND password=?",
            (email, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["role"] = user[1]

            if user[1] == "student":
                return redirect("/student")
            else:
                return redirect("/faculty")

        return "<h3 style='color:red;'>Invalid Credentials</h3>"

    return render_template("login.html")


# =========================
# STUDENT DASHBOARD
# =========================
@app.route("/student")
def student_dashboard():
    if session.get("role") != "student":
        return redirect("/")
    return render_template("student_dashboard.html")


# =========================
# FACULTY DASHBOARD
# =========================
@app.route("/faculty")
def faculty_dashboard():
    if session.get("role") != "faculty":
        return redirect("/")
    return render_template("faculty_dashboard.html")


# =========================
# GENERATE QR (FACULTY)
# =========================
@app.route("/generate_qr")
def generate_qr_route():
    if session.get("role") != "faculty":
        return redirect("/")

    print("➡️ Generate QR route hit")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sessions (faculty_id, subject, session_date, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        session["user_id"],
        "Regular Class",
        date.today().isoformat(),
        datetime.now().isoformat()
    ))

    session_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print("🆔 Session ID:", session_id)

    generate_qr(session_id)
    print("✅ QR generated")

    return render_template("faculty_dashboard.html", qr=True)


# =========================
# SCAN QR (STUDENT)
# =========================
@app.route("/scan_qr")
def scan_qr():
    if session.get("role") != "student":
        return redirect("/")
    return render_template("scan_qr.html")


# =========================
# MARK ATTENDANCE (STUDENT)
# =========================
@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    if session.get("role") != "student":
        return redirect("/")

    try:
        qr_data = request.form["qrdata"]
        data = json.loads(qr_data)
        session_id = data["session_id"]
    except:
        return "<h3>❌ Invalid QR Code</h3>"

    student_id = session["user_id"]

    conn = get_db()
    cursor = conn.cursor()

    # Prevent duplicate attendance for same session
    cursor.execute("""
        SELECT id FROM attendance
        WHERE student_id = ? AND session_id = ?
    """, (student_id, session_id))

    if cursor.fetchone():
        conn.close()
        return render_template("attendance_exists.html")

    cursor.execute("""
        INSERT INTO attendance (student_id, session_id, status)
        VALUES (?, ?, ?)
    """, (student_id, session_id, "Present"))

    conn.commit()
    conn.close()

    return render_template("attendance_success.html")


# =========================
# ATTENDANCE PERCENTAGE (STUDENT)
# =========================
@app.route("/attendance_percentage")
def attendance_percentage():
    if session.get("role") != "student":
        return redirect("/")

    student_id = session["user_id"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT session_id)
        FROM attendance
        WHERE student_id = ?
    """, (student_id,))
    attended = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sessions")
    total = cursor.fetchone()[0]

    conn.close()

    percentage = 0
    if total > 0:
        percentage = round(min((attended / total) * 100, 100), 2)

    return render_template(
        "attendance_percentage.html",
        attended=attended,
        total=total,
        percentage=percentage
    )


# =========================
# VIEW ATTENDANCE (FACULTY)
# =========================
@app.route("/view_attendance")
def view_attendance():
    if session.get("role") != "faculty":
        return redirect("/")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT users.name,
               sessions.session_date,
               attendance.status
        FROM attendance
        JOIN users ON users.id = attendance.student_id
        JOIN sessions ON sessions.id = attendance.session_id
        ORDER BY sessions.session_date DESC
    """)

    records = cursor.fetchall()
    conn.close()

    return render_template("view_attendance.html", records=records)


# =========================
# REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, ?)
            """, (name, email, password, role))
            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return """
            <h3 style="color:red;">⚠ Email already registered</h3>
            <a href="/register">Try another email</a>
            """

        conn.close()
        return redirect("/")

    return render_template("register.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
