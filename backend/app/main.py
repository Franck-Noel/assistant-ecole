from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest
from .ingest import indexer_les_pdfs
from .rag import obtenir_reponse

app = FastAPI(title="Backend Assistant ENSEA")

# Configuration CORS pour permettre la communication avec Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Indexation automatique des PDF au lancement
    indexer_les_pdfs()

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Appel de la logique RAG avec le mode choisi (Llama ou Gemini)
    reponse = obtenir_reponse(
        prompt=request.message, 
        history=request.history, 
        mode=request.mode
    )
    return {"response": reponse}