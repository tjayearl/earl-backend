from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import requests
import uuid

# Ollama API URL
OLLAMA_URL = "http://localhost:11434/api/generate"

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend domain if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory databases
chat_history = []
reminders = []

# Request models
class ChatRequest(BaseModel):
    message: str

class ReminderRequest(BaseModel):
    text: str

# Smart manual replies
def get_manual_response(msg: str) -> Optional[str]:
    msg = msg.lower()

    if "hello" in msg or "hi" in msg:
        return "Hey there! How can I assist you today?"
    elif "who are you" in msg:
        return "I'm E.A.R.L – your Enhanced Assistant for Real Life."
    elif "time" in msg:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
    elif "date" in msg:
        return f"Today is {datetime.now().strftime('%A, %d %B %Y')}."
    elif "bye" in msg or "goodbye" in msg:
        return "Goodbye! I'll be right here if you need anything else."
    elif "thank" in msg:
        return "You're always welcome!"
    elif "joke" in msg:
        return "Why don’t robots have brothers? Because they all share the same motherboard! 🤖"
    else:
        return None

# Use Ollama for AI responses
def get_ai_response(message: str) -> str:
    # Check manual response first
    manual = get_manual_response(message)
    if manual:
        return manual

    try:
        payload = {
            "model": "llama3",  # Change if using a different model
            "prompt": message,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)

        if response.status_code == 200:
            data = response.json()
            return data.get("response", "").strip()

        return f"⚠️ Ollama error: {response.status_code} - {response.text}"

    except requests.exceptions.ConnectionError:
        return "⚠️ E.A.R.L. could not connect to the local AI server."
    except Exception as e:
        return f"⚠️ E.A.R.L. had an error: {str(e)}"

# Routes
@app.post("/chat")
def chat(req: ChatRequest):
    user_msg = {"sender": "You", "text": req.message}
    reply_text = get_ai_response(req.message)
    ai_msg = {"sender": "E.A.R.L", "text": reply_text}
    chat_history.extend([user_msg, ai_msg])
    return {"reply": reply_text}

@app.get("/chat/history")
def get_chat_history():
    return chat_history

@app.get("/reminders")
def get_reminders():
    return reminders

@app.post("/reminders")
def add_reminder(req: ReminderRequest):
    reminder = {"id": str(uuid.uuid4()), "text": req.text}
    reminders.append(reminder)
    return reminder

@app.delete("/reminders/{reminder_id}")
def delete_reminder(reminder_id: str):
    global reminders
    reminders = [r for r in reminders if r["id"] != reminder_id]
    return {"status": "deleted"}

