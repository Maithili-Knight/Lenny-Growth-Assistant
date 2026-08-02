# 🚀 Lenny Growth Assistant — Production AI Chatbot & Artifact Studio

A production-grade, full-stack AI Growth Assistant built on **FastAPI**, **React + Vite**, **PostgreSQL**, **ChromaDB Vector Store**, and a multi-provider LLM engine supporting both **Anthropic Claude 3.5 Sonnet** (Cloud) and **Ollama** (Local).

The application features an agentic skills architecture (**Knowledge Q&A** vs. **Ship 30 for 30 Essay Generation**), a ChatGPT-identical dark mode UI with inline session renaming and auto-titling, and a Claude-style split-screen Artifact Viewer for rendering interactive HTML/CSS and Markdown essays.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            React + Vite Frontend                            │
│   (ChatGPT Dark Mode UI, Sidebar Session List, Double-Click Rename,          │
│    Model Switcher Pill, Claude Split-Screen Artifact Viewer)                │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │ HTTP REST / SSE Stream
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            FastAPI Backend Router                           │
│     (/chat/, /chat/stream, /sessions/, /messages/, /artifacts/)             │
└──────┬───────────────────────┬───────────────────────────────┬──────────────┘
       │                       │                               │
       ▼                       ▼                               ▼
┌──────────────┐      ┌─────────────────┐           ┌────────────────────┐
│  PostgreSQL  │      │ ChromaDB Vector │           │  Skills Classifier │
│  Database    │      │ Store           │           │  & RAG Engine      │
│ (Sessions,   │      │ (Lenny Podcast  │           │ (QA vs. Ship30     │
│  Messages,   │      │  Transcripts    │           │  Essay Skill)      │
│  Artifacts)  │      │  Embeddings)    │           └─────────┬──────────┘
└──────────────┘      └─────────────────┘                     │
                                                              ▼
                                                    ┌────────────────────┐
                                                    │ LLM Provider Layer │
                                                    │ (ollama_service.py │
                                                    │  & claude.py with  │
                                                    │  auto-fallback)    │
                                                    └────────────────────┘
```

### Component Details
1. **Frontend (React + Vite)**: Pure Vanilla CSS layout inspired by ChatGPT & Claude. Includes sidebar session management, inline title renaming, message streaming, and tabbed artifact previewing.
2. **FastAPI Backend**: Clean layered architecture adhering to SOLID principles:
   - `app/api/routes`: REST controller endpoints.
   - `app/crud`: Database operations for sessions, messages, and artifacts.
   - `app/services/skills.py`: Skill classifier and system prompt builder.
   - `app/services/llm_service.py`: Provider gateway (Claude Cloud / Ollama Local) with automatic fault-tolerant fallback.
3. **Database (PostgreSQL)**: Persistent storage for all user chat sessions, chronological message histories, and generated code/essay artifacts.
4. **Vector Database (ChromaDB)**: Stores embeddings of Lenny Rachitsky's podcast and newsletter transcripts for accurate Retrieval-Augmented Generation (RAG).

---

## 🌟 Key Features

* **Agentic Skill Routing**: Dynamically classifies user intent to switch between **Transcript Q&A** and **Ship 30 for 30 Essay Generation** (encoding 1/3/1 paragraph rhythm, bold hooks, and the 4A framework).
* **ChatGPT-Identical UI**: Dark mode theme (`#212121`), centered empty state welcome screen (*"Where should we begin?"*), auto-generated session titles from the first message, and double-click inline renaming.
* **Claude-Style Artifact Viewer**: Side-by-side split panel for reviewing code/essay artifacts with live sandboxed `iframe` rendering for HTML/CSS and rich Markdown previewing.
* **Dynamic Model Switcher**: Header dropdown allowing users to switch live between `⚡ Local (Ollama)` and `☁️ Cloud (Claude 3.5)`.
* **Automatic Fault Tolerance**: If Claude returns credit balance or API errors, the system automatically falls back to local Ollama without crashing.

---

## ⚙️ Prerequisites

- **Python**: `3.10` or higher
- **Node.js**: `v18` or higher
- **PostgreSQL**: Local PostgreSQL instance, Supabase, or Railway database URI
- **Ollama** *(Optional for local LLM)*: Installed and running locally (`ollama serve`) with model `llama3` or `mistral` pulled.

---

## 🔑 Environment Variables Setup

Create a `.env` file inside the `backend/` directory based on the template below.

> ⚠️ **SECURITY NOTICE**: Never commit your actual API keys or database password to Git!

```env
# app/core/config.py settings
APP_NAME="The Lenny Growth Assistant"
APP_VERSION="1.0.0"
DEBUG=True

# Database Configuration (PostgreSQL / Supabase / Railway)
DATABASE_URL="postgresql://postgres:your_password@localhost:5432/lenny_assistant"

# Default LLM Provider: "ollama" or "claude"
LLM_PROVIDER="ollama"

# Ollama Local Configuration
OLLAMA_BASE_URL="http://localhost:11434"
OLLAMA_MODEL="llama3"

# Anthropic Claude Configuration (Cloud)
# Leave empty if using local Ollama exclusively
ANTHROPIC_API_KEY="your_anthropic_api_key_here"

# Embedding Model (SentenceTransformers / HuggingFace)
EMBEDDING_MODEL="all-MiniLM-L6-v2"
```

---

## 🛠️ Step-by-Step Local Deployment Guide

### Step 1: Clone Repository
```bash
git clone https://github.com/Maithili-Knight/Lenny-Growth-Assistant.git
cd Lenny-Growth-Assistant
```

---

### Step 2: Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   * Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   * macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create `backend/.env` as shown in the Environment Variables section above.

5. **Populate ChromaDB Vector Database** *(Ingest transcripts)*:
   ```bash
   python -m app.services.build_vector_db
   ```

6. **Start the FastAPI Backend Server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   The backend API will be available at: `http://127.0.0.1:8000` (Interactive API docs at `http://127.0.0.1:8000/docs`).

---

### Step 3: Frontend Setup

1. **Open a new terminal and navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start Vite Development Server**:
   ```bash
   npm run dev
   ```

4. **Access Application**:
   Open your browser and navigate to `http://localhost:5173` (or the URL printed by Vite).

---

## 🧪 Verifying Test Cases

You can run automated verification checks for all API endpoints and skill routing logic:

```bash
cd backend
python -c "
import requests
r = requests.get('http://127.0.0.1:8000/sessions/')
print('Sessions status:', r.status_code)
"
```

To run a production frontend build:
```bash
cd frontend
npm run build
```

---

## 📄 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check endpoint |
| `POST` | `/chat/` | Synchronous chat endpoint (processes RAG, skills, auto-titles, & artifacts) |
| `POST` | `/chat/stream` | Token-by-token streaming chat endpoint |
| `GET` | `/sessions/` | Retrieves all chat sessions ordered by `created_at desc` |
| `POST` | `/sessions/` | Creates a new chat session |
| `PATCH` | `/sessions/{id}` | Renames a session title |
| `GET` | `/sessions/{id}/messages` | Fetches chronological message history for a session |
| `GET` | `/artifacts/{id}` | Fetches artifact details (title, type, content) |

---

## 📜 License & Credits

Built for the Lenny Growth Assistant Challenge. Transcripts courtesy of **Lenny Rachitsky's Podcast & Newsletter**. Ship30for30 framework inspired by **Dickie Bush & Nicolas Cole**.
