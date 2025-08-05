from flask import Flask, request, render_template_string, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Change this to your MySQL username
    password="sanJeev123!",  # Change this to your MySQL password
    database="suggestions_db"
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_info (
    student_id varchar(100) PRIMARY KEY,
    email char(100),
    password char(255)
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS suggestions (
    suggestion_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(100),
    department_name VARCHAR(100),
    suggestion_type VARCHAR(100),
    suggestion_text TEXT,
    FOREIGN KEY (student_id) REFERENCES student_info(student_id)
)
""")
conn.commit()

# Home route for signup page
@app.route('/')
def home():
    return render_template_string(open("signup.html", "r", encoding="utf-8").read())

# Signup form submission route
@app.route('/submit', methods=['POST'])
def submit():
    student_id = request.form['username']
    email = request.form["email"]
    password = request.form["password"]
    cursor.execute("INSERT INTO student_info (student_id, email, password) VALUES (%s, %s, %s)", (student_id, email, password))
    conn.commit()
    return redirect(url_for('signin'))  # Redirect to login page after signup

# Signin page
@app.route('/signin')
def signin():
    return render_template_string(open("index.html", "r", encoding="utf-8").read())

# Student dashboard page
@app.route('/stu_dash')
def stu_dash():
    return render_template_string(open("stu_dash.html", "r", encoding="utf-8").read())

# Signin form submission
@app.route('/submit_signin', methods=['POST'])
def submit_signin():
    student_id = request.form['student_id']
    password = request.form['password']

    cursor.execute("SELECT * FROM student_info WHERE student_id = %s", (student_id,))
    user = cursor.fetchone()

    if user:
        if password == user[2]:  # Check if the password matches
            return redirect(url_for('stu_dash'))  # Redirect to the student dashboard
        else:
            return "Incorrect password. Please try again."
    else:
        return "Student ID not found. Please check your Student ID."

# Route for submitting suggestions
@app.route('/submit_suggestion', methods=['POST'])
def submit_suggestion():
    student_id = request.form['student_id']
    department_name = request.form['department_name']
    suggestion_type = request.form['suggestion_type']
    suggestion_text = request.form['suggestion_text']

    cursor.execute("""
    INSERT INTO suggestions (student_id, department_name, suggestion_type, suggestion_text)
    VALUES (%s, %s, %s, %s)
    """, (student_id, department_name, suggestion_type, suggestion_text))
    conn.commit()
    return "Your suggestion has been submitted successfully!"

# Route for the suggestion form
@app.route('/suggestions_form')
def suggestions_form():
    return render_template_string(open("suggestion_form.html", "r", encoding="utf-8").read())

if __name__ == '__main__':
    app.run(debug=True)
