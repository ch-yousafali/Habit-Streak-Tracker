# Habit Streak Tracker

A minimal Flask-based exercise tracker for marking completed days and reviewing progress month-by-month.

## Features

- Personalized tracker with user name entry.
- Clickable calendar days to mark exercise completion.
- Monthly summary with completed days, productivity percentage, and active weeks.
- Minimal modern UI with month navigation.
- Data saved locally in `habits.json`.

## Files

- `main.py` — Flask application logic and data management.
- `templates/index.html` — HTML template and styles for the dashboard.
- `habits.json` — Local JSON storage for user name and completed dates.

## Requirements

- Python 3
- Flask

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install Flask
python3 main.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Usage

1. Enter your name on first load.
2. Click calendar dates to mark exercise as complete.
3. Use the month navigation buttons to switch months.
4. Review the monthly activity graph and summary.

## Notes

- The app stores progress locally in `habits.json`.
- Refreshing the page after toggling a day updates the calendar state.

## Architecture

```
+-----------+                +---------------------+                +-------------+
|  Web UI   | -------------> |       Backend       | -------------> | Data Storage|
|           |  User Action   |      (main.py)      |  Read/Write    |             |
| (Browser) | <------------- |                     | <------------- |(habits.json)|
+-----------+  Updated View  | - Handle Requests   |                +-------------+
                             | - Calculate Streaks |
                             +---------------------+
```
