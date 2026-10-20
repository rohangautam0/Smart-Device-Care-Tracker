from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps
from werkzeug.security import check_password_hash
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH", "")

DATA_FILE = "repairs.json"

STATUSES = [
    "Received",
    "In Progress",
    "Ready for Pickup",
    "Delivered"
]


def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view_function(*args, **kwargs)
    return wrapped_view


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if (
            ADMIN_PASSWORD_HASH
            and username == ADMIN_USERNAME
            and check_password_hash(ADMIN_PASSWORD_HASH, password)
        ):
            session["logged_in"] = True
            return redirect(url_for("home"))

        error = "Invalid username or password."

    return render_template("login.html", error=error)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


def load_repairs():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_repairs(repairs):
    with open(DATA_FILE, "w") as file:
        json.dump(repairs, file, indent=4)


@app.route("/")
@login_required
def home():
    repairs = load_repairs()
    search_query = request.args.get("search", "").strip().lower()

    if search_query:
        repairs = [
            repair for repair in repairs
            if isinstance(repair, dict) and (
                search_query in repair.get("customer", "").lower()
                or search_query in repair.get("device", "").lower()
                or search_query in repair.get("problem", "").lower()
            )
        ]

    return render_template(
        "index.html",
        repairs=repairs,
        statuses=STATUSES,
        search_query=search_query
    )


@app.route("/add", methods=["POST"])
@login_required
def add_repair():
    repairs = load_repairs()

    new_repair = {
        "customer": request.form.get("customer", "").strip(),
        "device": request.form.get("device", "").strip(),
        "problem": request.form.get("problem", "").strip(),
        "status": "Received"
    }

    if all(new_repair[key] for key in ["customer", "device", "problem"]):
        repairs.append(new_repair)
        save_repairs(repairs)

    return redirect(url_for("home"))


@app.route("/update/<int:repair_id>", methods=["POST"])
@login_required
def update_status(repair_id):
    repairs = load_repairs()
    new_status = request.form.get("status", "")

    if 0 <= repair_id < len(repairs) and new_status in STATUSES:
        repair = repairs[repair_id]

        if isinstance(repair, dict):
            repair["status"] = new_status
            save_repairs(repairs)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)