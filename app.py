import sqlite3
from flask import Flask
from flask import flash, abort, redirect, render_template, request, session
import config
import db
import tasks
import users
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    open_tasks = tasks.get_pending_tasks()
    done_tasks = tasks.get_completed_tasks()
    return render_template("index.html", tasks=open_tasks, completed_tasks=done_tasks)

@app.route("/task/<int:task_id>")
def show_task(task_id):
    task = tasks.get_task(task_id)
    if not task:
        abort(404)
    progress_list = tasks.get_progress(task_id)
    return render_template("show_task.html", task=task, progress_list=progress_list)

@app.route("/find_task")
def find_task():
    query = request.args.get("query")
    if query:
        results = tasks.find_tasks(query)
    else:
        query = ""
        results = []
    return render_template("find_task.html", query=query, results=results)

@app.route("/new_task")
def new_task():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("new_task.html", current_date=date.today().isoformat())

@app.route("/create_task", methods=["POST"])
def create_task():
    require_login()
    title = request.form["title"]
    if not title or len(title) > 50:
        return "VIRHE: otsikko saa olla enintään 50 merkkiä pitkä"
    description = request.form["description"]
    if not description or len(description) > 1000:
        return "VIRHE: kuvaus saa olla enintään 1000 merkkiä pitkä"
    priority = request.form["priority"]
    due_date = request.form.get("due_date")
    if not due_date:
        flash("Määräaika puuttuu.")
        return redirect("/new_task")
    due = datetime.strptime(due_date, "%Y-%m-%d").date()
    if due < date.today():
        flash("Määräaika ei voi olla menneisyydessä.")
        return redirect("/new_task")
    user_id = session.get("user_id")

    tasks.add_task(title, description, priority, due_date, user_id)

    return redirect("/")

@app.route("/edit_task/<int:task_id>")
def edit_task(task_id):
    require_login()
    task = tasks.get_task(task_id)
    if not task:
        abort(404)
    if task["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_task.html", task=task, current_date=date.today().isoformat())

@app.route("/update_task", methods=["POST"])
def update_task():
    require_login()
    task_id = request.form["task_id"]
    task = tasks.get_task(task_id)
    if not task:
        abort(404)
    if task["user_id"] != session["user_id"]:
        abort(403)
    title = request.form["title"]
    if not title or len(title) > 50:
        return "VIRHE: otsikko saa olla enintään 50 merkkiä pitkä"
    description = request.form["description"]
    if not description or len(description) > 1000:
        return "VIRHE: kuvaus saa olla enintään 1000 merkkiä pitkä"
    priority = request.form["priority"]
    due_date = request.form.get("due_date")
    if not due_date:
        flash("Määräaika puuttuu.")
        return redirect(f"/edit_task/{task_id}")
    due = datetime.strptime(due_date, "%Y-%m-%d").date()
    if due < date.today():
        flash("Määräaika ei voi olla menneisyydessä.")
        return redirect(f"/edit_task/{task_id}")

    tasks.update_task(task_id, title, description, priority, due_date)

    return redirect("/task/" + str(task_id))

@app.route("/remove_task/<int:task_id>", methods=["GET", "POST"])
def remove_task(task_id):
    require_login()
    task = tasks.get_task(task_id)
    if not task:
        abort(404)
    if task["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove_task.html", task=task)
    if request.method == "POST":
        if "remove" in request.form:
            tasks.remove_task(task_id)
            return redirect("/")
        else:
            return redirect("/task/" + str(task_id))

@app.route("/complete_task/<int:task_id>", methods=["GET", "POST"])
def complete_task(task_id):
    if request.method == "GET":
        task = tasks.get_task(task_id)
        return render_template("complete_task.html", task=task)

    if request.method == "POST":
        if "complete" in request.form:
            tasks.mark_task_completed(task_id)
            return redirect("/")
        else:
            return redirect("/task/" + str(task_id))

@app.route("/uncomplete_task/<int:task_id>", methods=["GET", "POST"])
def uncomplete_task(task_id):
    if request.method == "GET":
        task = tasks.get_task(task_id)
        return render_template("uncomplete_task.html", task=task)

    if request.method == "POST":
        if "uncomplete" in request.form:
            tasks.mark_task_pending(task_id)
            return redirect("/")
        else:
            return redirect("/task/" + str(task_id))

@app.route("/add_progress/<int:task_id>", methods=["POST"])
def add_progress(task_id):
    if "user_id" not in session:
        return redirect("/login")

    content = request.form["content"]
    if not content.strip():
        return redirect(f"/task/{task_id}")

    tasks.add_progress(task_id, session["user_id"], content)
    return redirect(f"/task/{task_id}")

@app.route("/delete_progress/<int:progress_id>", methods=["POST"])
def delete_progress_route(progress_id):
    pr = tasks.get_one(progress_id)
    if not pr:
        abort(404)
    if pr["user_id"] != session.get("user_id"):
        abort(403)
    tasks.delete_progress(progress_id)
    return redirect(f"/task/{pr['task_id']}")

@app.route("/edit_progress/<int:progress_id>")
def edit_progress(progress_id):
    pr = tasks.get_one(progress_id)
    if not pr:
        abort(404)

    if pr["user_id"] != session.get("user_id"):
        abort(403)

    return render_template("edit_progress.html", pr=pr)

@app.route("/edit_progress/<int:progress_id>", methods=["POST"])
def update_progress_route(progress_id):
    pr = tasks.get_one(progress_id)
    if not pr:
        abort(404)

    if pr["user_id"] != session.get("user_id"):
        abort(403)

    content = request.form["content"]
    tasks.update_progress(progress_id, content)
    return redirect(f"/task/{pr['task_id']}")

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

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo olemassa"

    #return "Tunnus luotu onnistuneesti" #Alkuperäinen vastaus tunnuksen luomisen jälkeen, loi kuitenkin ongelman miten käyttäjä pääsi etusivulle
    return redirect("/login")  #Uusi vastaus, ohjaa käyttäjän kirjautumissivulle, mutta onnistumisviesti puuttuu

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)

        if user_id:
            session["user_id"] = int(user_id)
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.route("/my_page")
def my_page():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    username = session["username"]
    return render_template("my_page.html", user_id=user_id, username=username)

@app.route("/profile/<int:user_id>")
def profile(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    open_tasks = users.get_pending_tasks(user_id)
    done_tasks = users.get_completed_tasks(user_id)
    return render_template("profile.html", user=user, tasks=open_tasks, completed_tasks=done_tasks)
