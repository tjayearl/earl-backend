from fastapi import APIRouter
from pydantic import BaseModel
from services.ollama_service import ask_ollama

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_with_earl(request: ChatRequest):
    return {"response": ask_ollama(request.message)}

