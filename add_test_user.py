import sqlite3

conn = sqlite3.connect("database/attendance.db")
cursor = conn.cursor()

# Insert FACULTY user
cursor.execute("""
INSERT INTO users (name, email, password, role)
VALUES (?, ?, ?, ?)
""", ("Test Faculty", "faculty@test.com", "faculty123", "faculty"))

# Insert STUDENT user
cursor.execute("""
INSERT INTO users (name, email, password, role)
VALUES (?, ?, ?, ?)
""", ("Test Student", "student@test.com", "student123", "student"))

conn.commit()
conn.close()

print("✅ Test users added successfully")
