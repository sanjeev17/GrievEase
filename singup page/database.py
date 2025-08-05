from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this

# MySQL Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://student_user:sanJeev123!@localhost/student_system"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Hashed Password

# Route: Sign-Up
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validation
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("signup"))

        # Hash password
        hashed_password = generate_password_hash(password)

        # Store in DB
        new_student = Student(name=name, email=email, password=hashed_password)
        try:
            db.session.add(new_student)
            db.session.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("login"))
        except:
            db.session.rollback()
            flash("Email already exists!", "danger")

    return render_template("signup.html")

# Route: Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        student = Student.query.filter_by(email=email).first()

        if student and check_password_hash(student.password, password):
            session["student_id"] = student.id
            session["name"] = student.name
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Email or Password!", "danger")

    return render_template("login.html")

# Route: Dashboard (Protected)
@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    return f"<h1>Welcome, {session['name']}! This is your Dashboard.</h1>"

# Route: Logout
@app.route("/logout")
def logout():
    session.pop("student_id", None)
    session.pop("name", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# Create Database Tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
