# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.openai_service import ask_e_a_r_l
from services.logger import log_chat
import os

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chat request model
class ChatRequest(BaseModel):
    prompt: str
    mode: str = "default"
    model: str = "gpt-4o"

@app.post("/chat")
def chat_with_earl(request: ChatRequest):
    response = ask_e_a_r_l(request.prompt, request.mode, request.model)
    log_chat(request.prompt, response)
    return {"response": response}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    # Save file to local dir (optional: process it)
    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(content)
    return {"filename": file.filename, "message": "Upload successful"}

