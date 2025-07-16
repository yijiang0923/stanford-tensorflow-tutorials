from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import json
from datetime import datetime
import uvicorn

app = FastAPI(title="Desktop LLM Server", version="1.0.0")

# Enable CORS for iOS app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your iOS app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    conversation_history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime

# Store conversation history (in production, use a database)
conversations = {}

# TODO: Replace this with your actual LLM integration
async def generate_llm_response(prompt: str, history: List[ChatMessage]) -> str:
    """
    Replace this function with your actual LLM integration.
    This could be:
    - OpenAI API calls
    - Local model inference (transformers, llama.cpp, etc.)
    - Ollama integration
    - Any other LLM service
    """
    # Simulate LLM processing time
    await asyncio.sleep(1)
    
    # Mock response - replace with actual LLM call
    responses = [
        f"I understand you said: '{prompt}'. How can I help you further?",
        f"That's an interesting question about '{prompt}'. Let me think about that.",
        f"Regarding '{prompt}', here's what I think...",
        f"I'd be happy to help with '{prompt}'. Here's my response:",
    ]
    
    # Simple mock logic based on prompt
    if "hello" in prompt.lower():
        return "Hello! How can I assist you today?"
    elif "weather" in prompt.lower():
        return "I don't have access to real-time weather data, but I can help you with other questions!"
    elif "code" in prompt.lower():
        return "I'd be happy to help with coding questions. What programming language are you working with?"
    else:
        return responses[len(history) % len(responses)]

@app.get("/")
async def root():
    return {"message": "Desktop LLM Server is running!", "status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Generate response using your LLM
        response = await generate_llm_response(request.message, request.conversation_history)
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.delete("/conversations/{conversation_id}")
async def clear_conversation(conversation_id: str):
    if conversation_id in conversations:
        del conversations[conversation_id]
    return {"message": "Conversation cleared"}

if __name__ == "__main__":
    # Run with: python main.py
    uvicorn.run(app, host="0.0.0.0", port=8000)