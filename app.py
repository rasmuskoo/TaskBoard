import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import tasks

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    tasks.get_tasks()
    return render_template("index.html", tasks=tasks.get_tasks())

@app.route("/task/<int:task_id>")
def show_task(task_id):
    task = tasks.get_task(task_id)
    return render_template("show_task.html", task=task)

@app.route("/new_task")
def new_task():
    return render_template("new_task.html")

@app.route("/create_task", methods=["POST"])
def create_task():
    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    due_date = request.form["due_date"]
    user_id = session.get("user_id")

    tasks.add_task(title, description, priority, due_date, user_id)

    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät täsmää"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo olemassa"

    return "Tunnus luotu onnistuneesti"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")