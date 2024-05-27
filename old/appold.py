# from flask import (
#     Flask,
#     request,
#     render_template,
#     redirect,
#     url_for,
#     jsonify,
#     flash,
#     make_response,
# )
# from flask_mysqldb import MySQL
# from flask_login import (
#     LoginManager,
#     UserMixin,
#     login_user,
#     login_required,
#     logout_user,
#     current_user,
# )
# from flask_bcrypt import Bcrypt
# import os
# import csv
# import io
# from werkzeug.utils import secure_filename
# from datetime import date
# import base64
# import re

# app = Flask(__name__)
# app.config["SECRET_KEY"] = "your_secret_key"
# app.config["MYSQL_HOST"] = "localhost"
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = "12345"
# app.config["MYSQL_DB"] = "pms_db"
# app.config["UPLOAD_FOLDER"] = "static/uploads/"

# mysql = MySQL(app)
# login_manager = LoginManager(app)
# login_manager.login_view = "login"
# bcrypt = Bcrypt(app)


# class User(UserMixin):
#     def __init__(self, id, username, password):
#         self.id = id
#         self.username = username
#         self.password = password


# @login_manager.user_loader
# def load_user(user_id):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
#     user = cur.fetchone()
#     cur.close()
#     if user:
#         return User(id=user[0], username=user[1], password=user[2])
#     return None


# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

#         cur = mysql.connection.cursor()
#         cur.execute(
#             "INSERT INTO users (username, password) VALUES (%s, %s)",
#             (username, hashed_password),
#         )
#         mysql.connection.commit()
#         cur.close()

#         flash("Account created successfully! You can now log in.", "success")
#         return redirect(url_for("login"))

#     return render_template("signup.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM users WHERE username = %s", (username,))
#         user = cur.fetchone()
#         cur.close()
#         if user and bcrypt.check_password_hash(user[2], password):
#             login_user(User(id=user[0], username=user[1], password=user[2]))
#             return jsonify({"success": True, "message": "Login successful"})

#         flash("Login Unsuccessful. Please check username and password", "danger")
#     return render_template("login.html")


# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("login"))


# @app.route("/")
# @login_required
# def index():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM patients")
#     patients = cur.fetchall()
#     cur.close()
#     return render_template("index.html", patients=patients)


# @app.route("/add_patient", methods=["GET", "POST"])
# @login_required
# def add_patient():
#     if request.method == "POST":
#         name = request.form["name"]
#         birthday = request.form["birthday"]
#         age = request.form["age"]
#         gender = request.form["gender"]
#         contact = request.form["contact"]

#         photo_data = request.form["photo"]

#         img_data = re.sub("^data:image/.+;base64,", "", photo_data)
#         img_data = base64.b64decode(img_data)
#         photo_filename = secure_filename(f"{name}_{birthday}.jpg")

#         photo_filename = secure_filename(photo_filename)
#         photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo_filename)

#         with open(photo_path, "wb") as f:
#             f.write(img_data)
#         cur = mysql.connection.cursor()
#         cur.execute(
#             "INSERT INTO patients (name, birthday, age, gender, contact, photo) VALUES (%s, %s, %s, %s, %s, %s)",
#             (name, birthday, age, gender, contact, photo_filename),
#         )
#         mysql.connection.commit()
#         cur.close()
#         flash("Patient added successfully!", "success")
#         return redirect(url_for("index"))

#     return render_template("add_patient.html")


# @app.route("/search_patient", methods=["GET", "POST"])
# @login_required
# def search_patient():
#     if request.method == "POST":
#         birthday = request.form["birthday"]
#         print(birthday)
#         cur = mysql.connection.cursor()
#         cur.execute(
#             "SELECT id, name, birthday FROM patients WHERE birthday = %s", [birthday]
#         )
#         patients = cur.fetchall()
#         cur.close()
#         # print(patients)
#         if not request.is_json:
#             return jsonify(patients=patients)

#         # return render_template('search_patient.html' ,patients=patients)

#     return render_template("search_patient.html")


# @app.route("/add_record/<int:patient_id>", methods=["GET", "POST"])
# @login_required
# def add_record(patient_id):
#     if request.method == "POST":
#         record_date = request.form["record_date"]
#         complaints = request.form["complaints"]
#         history = request.form["history"]
#         diagnosed = request.form["diagnosed"]
#         treatment = request.form["treatment"]
#         next_review = request.form["next_review"]
#         charges = request.form["charges"]
#         cur = mysql.connection.cursor()
#         cur.execute(
#             "INSERT INTO medical_records (patient_id, record_date, complaints, history, diagnosed, treatment, next_review,charges) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",
#             (
#                 patient_id,
#                 record_date,
#                 complaints,
#                 history,
#                 diagnosed,
#                 treatment,
#                 next_review,
#                 charges,
#             ),
#         )

#         mysql.connection.commit()
#         cur.close()
#         return redirect(url_for("index"))
#     return render_template("add_record.html", patient_id=patient_id)


# def fetch_daily_report():
#     cur = mysql.connection.cursor()
#     today = date.today()
#     cur.execute(
#         "SELECT p.name AS patient_name , charges FROM pms_db.patients p INNER JOIN pms_db.medical_records mr ON p.id = mr.patient_id WHERE record_date = %s",
#         (today,),
#     )
#     records = cur.fetchall()
#     cur.close()
#     return records


# def get_total_charges():
#     cur = mysql.connection.cursor()
#     today = date.today()
#     cur.execute(
#         "SELECT SUM(charges) as total FROM medical_records WHERE record_date = %s",
#         (today,),
#     )
#     t = cur.fetchall()
#     cur.close()
#     return t


# @app.route("/get_daily_report")
# @login_required
# def get_daily_report():
#     records = fetch_daily_report()
#     total = get_total_charges()
#     return jsonify(records=records, total=total)


# @app.route("/daily_report")
# def daily_report():
#     return render_template("daily_report.html")


