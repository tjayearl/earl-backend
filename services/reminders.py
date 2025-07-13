import json
import os

REMINDERS_FILE = "db/reminders.json"

if not os.path.exists(REMINDERS_FILE):
    with open(REMINDERS_FILE, "w") as f:
        json.dump([], f)

def add_reminder(text):
    with open(REMINDERS_FILE, "r") as f:
        reminders = json.load(f)
    reminders.append({"text": text})
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f)
    return {"message": "Reminder added"}

def get_reminders():
    with open(REMINDERS_FILE, "r") as f:
        return json.load(f)
