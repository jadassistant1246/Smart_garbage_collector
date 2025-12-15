from flask import Flask, request, render_template, redirect, url_for, session

import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jadhav@1234",
        database="collector"
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(15),
            vehicle_no VARCHAR(20),
            address TEXT,
            email VARCHAR(100) UNIQUE,
            area VARCHAR(50),
            password VARCHAR(255)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user and password(user["password"], password):
            session["username"] = user["name"]
            return redirect(url_for("index"))

        return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        vehicle_no = request.form["vehicle_no"]
        address = request.form["address"]
        email = request.form["email"]
        area = request.form["area"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing = cur.fetchone()

        if existing:
            cur.close()
            conn.close()
            return render_template("register.html", error="User already exists")

        cur.execute(
            "INSERT INTO users(name, phone, vehicle_no, address, email, area, password) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (name, phone, vehicle_no, address, email, area, password)
        )

        conn.commit()
        cur.close()
        conn.close()

        session["username"] = name
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/index")
def index():
    if "username" in session:
        return render_template("index.html", username=session["username"])
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


@app.route("/")
def home():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)