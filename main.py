import json
from datetime import datetime, date
from calendar import monthrange
from flask import Flask, render_template, request, jsonify, redirect

app = Flask(__name__)
DATA_FILE = "habits.json"

def load_data():
    today = date.today()
    default_habit = {
        "id": "exercise",
        "name": "Exercise",
        "createdAt": today.strftime("%Y-%m-%d"),
        "history": []
    }
    default_data = {"user": {"name": ""}, "habit": default_habit}

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return default_data

    if isinstance(data, dict) and "habits" in data:
        habit = data["habits"][0] if data["habits"] else default_habit
        user = data.get("user", {"name": ""})
        return {"user": user, "habit": habit}

    data.setdefault("user", {"name": ""})
    data.setdefault("habit", default_habit)
    return data


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def parse_month_query(month_value):
    today = date.today()
    try:
        year_str, month_str = month_value.split("-")
        return date(int(year_str), int(month_str), 1)
    except Exception:
        return date(today.year, today.month, 1)


def month_navigation(month_date, offset):
    year = month_date.year
    month = month_date.month + offset
    while month < 1:
        month += 12
        year -= 1
    while month > 12:
        month -= 12
        year += 1
    return f"{year:04d}-{month:02d}"


def build_month_calendar(month_date, history_set):
    year = month_date.year
    month = month_date.month
    first_day = date(year, month, 1)
    first_weekday = (first_day.weekday() + 1) % 7
    total_days = monthrange(year, month)[1]
    slots = []

    for _ in range(first_weekday):
        slots.append(None)

    for day in range(1, total_days + 1):
        current_day = date(year, month, day)
        day_str = current_day.strftime("%Y-%m-%d")
        slots.append({"date": current_day, "done": day_str in history_set})

    while len(slots) % 7 != 0:
        slots.append(None)

    weeks = [slots[i:i + 7] for i in range(0, len(slots), 7)]
    weekly_counts = [sum(1 for day in week if day and day["done"]) for week in weeks]
    return weeks, weekly_counts, total_days


def month_activity_summary(month_date, history):
    days_done = 0
    active_weeks = set()
    for day_string in history:
        try:
            day_value = datetime.strptime(day_string, "%Y-%m-%d").date()
        except ValueError:
            continue
        if day_value.year == month_date.year and day_value.month == month_date.month:
            days_done += 1
            active_weeks.add((day_value.isocalendar()[0], day_value.isocalendar()[1]))
    return days_done, len(active_weeks)


@app.route("/")
def home():
    data = load_data()
    month_value = request.args.get("month", date.today().strftime("%Y-%m"))
    month_date = parse_month_query(month_value)
    history_set = set(data["habit"].get("history", []))
    weeks, weekly_counts, total_days = build_month_calendar(month_date, history_set)
    days_done, active_weeks = month_activity_summary(month_date, data["habit"].get("history", []))
    month_progress = round(days_done * 100 / total_days) if total_days else 0
    chart_data = [
        {"label": f"W{i + 1}", "count": count, "percent": round(count * 100 / 7)}
        for i, count in enumerate(weekly_counts)
    ]

    return render_template(
        "index.html",
        user=data["user"],
        habit=data["habit"],
        current_month=month_date.strftime("%B %Y"),
        month_value=month_date.strftime("%Y-%m"),
        prev_month=month_navigation(month_date, -1),
        next_month=month_navigation(month_date, 1),
        weeks=weeks,
        chart_data=chart_data,
        days_done=days_done,
        active_weeks=active_weeks,
        total_days=total_days,
        month_progress=month_progress,
    )


@app.route("/save-name", methods=["POST"])
def save_name():
    data = load_data()
    name = request.form.get("name", "").strip()
    if name:
        data["user"] = {"name": name}
        save_data(data)
    return redirect("/")


@app.route("/toggle-day", methods=["POST"])
def toggle_day():
    data = load_data()
    day = request.json.get("date")
    history = set(data["habit"].get("history", []))
    if day in history:
        history.remove(day)
    else:
        history.add(day)
    data["habit"]["history"] = sorted(history)
    save_data(data)
    return jsonify(success=True, date=day)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
