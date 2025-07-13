from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

app = FastAPI()

# Enable CORS for frontend (customize this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory databases
chat_history = []
reminders = []

# Models
class ChatRequest(BaseModel):
    message: str

class ReminderRequest(BaseModel):
    text: str

class Reminder(BaseModel):
    id: str
    text: str

# SMART CHAT LOGIC
def get_ai_response(message: str) -> str:
    msg = message.lower()

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
        return "Hmm... I didn’t quite get that. Try asking me about the time, date, or who I am!"

# Routes
@app.post("/chat")
def chat(req: ChatRequest):
    user_msg = {"sender": "You", "text": req.message}
    reply_text = get_ai_response(req.message)
    ai_msg = {"sender": "E.A.R.L", "text": reply_text}

    chat_history.extend([user_msg, ai_msg])
    return {"reply": reply_text}

@app.get("/chat/history")
def get_chat():
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

