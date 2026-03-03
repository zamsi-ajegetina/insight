"""FastAPI web application with LangChain RAG backend."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

from app.config import settings
from app.rag.chain import generate_answer

# Initialize FastAPI
app = FastAPI(
    title="Meridian Policy Assistant (LangChain)",
    description="RAG Policy Q&A API built with FastAPI and LangChain",
    version="2.0.0"
)

# Initialize Jinja2 templates (using the copied index.html)
templates = Jinja2Templates(directory=str(settings.PROJECT_ROOT / "app" / "templates"))

# Define request/response models
class ChatRequest(BaseModel):
    question: str

class Citation(BaseModel):
    document: str
    section: str = ""
    snippet: str = ""

class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation] = []
    error: str = None


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    """Serve the chat UI."""
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle a user question and return an answer with citations."""
    question = request.question.strip()
    
    if not question:
        return ChatResponse(
            answer="",
            error="No question provided."
        )
        
    # Run the LangChain pipeline
    result = generate_answer(question)
    
    if "Error:" in result.get("answer", ""):
        return ChatResponse(
            answer=result.get("answer"),
            error=result.get("answer")
        )
        
    return ChatResponse(
        answer=result.get("answer", ""),
        citations=[Citation(**c) for c in result.get("citations", [])]
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "version": app.version,
        "framework": "fastapi+langchain"
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
