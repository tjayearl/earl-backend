from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev: allow all, change in production
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

# Routes
@app.post("/chat")
def chat(req: ChatRequest):
    user_msg = {"sender": "You", "text": req.message}
    ai_reply = {"sender": "E.A.R.L", "text": f"Hello! You said: {req.message}"}
    chat_history.extend([user_msg, ai_reply])
    return {"reply": ai_reply["text"]}

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
