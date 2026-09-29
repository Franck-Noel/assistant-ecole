# Assistant ENSEA (version Gemini)

Chatbot RAG qui répond aux questions sur l'école à partir de documents PDF.
Backend FastAPI + ChromaDB, modèle Gemini 2.5 Flash, interface Streamlit.

## Structure

- `backend/` : API FastAPI (`/chat`), indexation des PDF et logique RAG
- `frontend/` : interface Streamlit
- `documents_ecole/` : documents sources (PDF) indexés au démarrage

## Installation

```bash
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r backend/requirements.txt
```

## Clé API Gemini

Crée une clé sur https://aistudio.google.com/apikey puis :

```bash
export GENAI_API_KEY="ta_cle"          # Windows PowerShell : $env:GENAI_API_KEY="ta_cle"
```

Ne mets jamais la clé dans le code. Voir `.env.example`.

## Lancement

Backend (depuis le dossier `backend/`, l'indexation des PDF se fait au démarrage) :

```bash
cd backend
uvicorn app.main:app --reload
```

Frontend (dans un second terminal, avec la même clé si besoin) :

```bash
cd frontend
streamlit run ui.py
```
