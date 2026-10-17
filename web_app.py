from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "repairs.json"

STATUSES = [
    "Received",
    "In Progress",
    "Ready for Pickup",
    "Delivered"
]


def load_repairs():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_repairs(repairs):
    with open(DATA_FILE, "w") as file:
        json.dump(repairs, file, indent=4)


@app.route("/")
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

    return redirect("/")


@app.route("/update/<int:repair_id>", methods=["POST"])
def update_status(repair_id):
    repairs = load_repairs()
    new_status = request.form.get("status", "")

    if 0 <= repair_id < len(repairs) and new_status in STATUSES:
        repair = repairs[repair_id]

        if isinstance(repair, dict):
            repair["status"] = new_status
            save_repairs(repairs)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)