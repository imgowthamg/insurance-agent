# 🛡️ Insurance Agentic AI

A multi-agent insurance policy query system built with **LangGraph**, **RAG**, **ChromaDB**, and **Gemma3:1b** via Ollama. Ask any question about your insurance policy and get a structured decision with a full report.

---

## 🏗️ Architecture

```
User Question
     │
     ▼
┌─────────────┐
│ Intent Agent│  → Classifies the query
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Retriever Agent  │  → Searches ChromaDB (RAG)
└──────┬───────────┘
       │ (no context → END)
       ▼
┌──────────────────┐
│  Policy Agent    │  → Extracts relevant clauses
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Decision Agent   │  → Returns JSON verdict
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Report Agent    │  → Generates clean markdown report
└──────────────────┘
```

---

## 🚀 Quick Start (Docker)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/insurance-agent.git
cd insurance-agent
```

### 2. Start all containers
```bash
docker compose up -d --build
```

### 3. Pull the LLM model
```bash
docker compose exec ollama ollama pull gemma3:1b
```

### 4. Load your policy documents
```bash
docker compose exec api python -c "
from app.rag import store_chunks

chunks = [
    'Your policy text chunk 1...',
    'Your policy text chunk 2...',
]
store_chunks(chunks)
print('Done!')
"
```

### 5. Open the UI
Open `ui.html` in your browser — it connects to `http://localhost:8000` automatically.

Or use the Swagger docs at **http://localhost:8000/docs**

---

## 📁 Project Structure

```
insurance-agent/
├── app/
│   ├── __init__.py
│   ├── agents.py       # 5 LangGraph agents
│   ├── graph.py        # LangGraph workflow
│   ├── llm.py          # Ollama LLM config
│   ├── main.py         # FastAPI app
│   └── rag.py          # ChromaDB + embeddings
├── ui.html             # Frontend UI
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .dockerignore
```

---

## 🔌 API

### `POST /analyze`

**Request:**
```json
{
  "question": "Is dental care covered?"
}
```

**Response:**
```json
{
  "question": "Is dental care covered?",
  "decision": {
    "decision": "Approved",
    "reason": "Dental care is covered for basic treatments up to INR 10,000 per year."
  },
  "final_answer": "## Insurance Report\n..."
}
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agents & Workflow | LangGraph |
| LLM | Gemma3:1b via Ollama |
| Vector DB | ChromaDB |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| API | FastAPI |
| Containerization | Docker + Docker Compose |

---

## 🐳 Docker Commands

```bash
# Start
docker compose up -d

# Stop
docker compose down

# View logs
docker compose logs -f api

# Rebuild after code changes
docker compose up -d --build api
```

---

## 📄 License

MIT
