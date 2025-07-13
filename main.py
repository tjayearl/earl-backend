from fastapi import FastAPI
from pydantic import BaseModel
from services.openai_service import ask_e_a_r_l
from services.language_detection import detect_language

app = FastAPI(title="E.A.R.L. - Enhanced Assistant for Real Life")

class Query(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "Welcome to E.A.R.L. - Your AI Assistant"}

@app.post("/chat")
def chat(query: Query):
    user_message = query.message
    language = detect_language(user_message)
    reply = ask_e_a_r_l(user_message)

    return {
        "user_message": user_message,
        "detected_language": language,
        "earl_reply": reply
    }
