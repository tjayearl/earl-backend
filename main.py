from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uuid
import openai
from datetime import datetime

# Load .env variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# Smart manual replies
def get_manual_response(msg: str) -> str | None:
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

# Use OpenAI's updated chat interface (v1.x)
def get_ai_response(message: str) -> str:
    manual = get_manual_response(message)
    if manual:
        return manual

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # or gpt-4 if upgraded
            messages=[
                {"role": "system", "content": "You are E.A.R.L, a helpful, polite, and intelligent personal assistant."},
                {"role": "user", "content": message},
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI Error:", e)
        return "⚠️ I'm having trouble thinking right now. Try again later."

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

