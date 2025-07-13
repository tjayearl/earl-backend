import json
from datetime import datetime

LOG_FILE = "db/chat_log.json"

def log_chat(prompt, response):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response
    }
    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)
