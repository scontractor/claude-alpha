# 🧠 Personal Knowledge Base

A local AI-powered knowledge base that lets you upload documents and ask questions about them — privately, on your own machine.

---

## What it does

- **Upload documents** (PDF, DOCX, Markdown, TXT) via drag-and-drop in the browser
- **Search** your documents semantically — finds relevant content even if you don't use exact keywords
- **Ask questions** in natural language and get AI-generated answers with cited sources
- **Manage documents** — see what's ingested and delete individual files at any time
- Everything runs **locally** — your documents never leave your machine

---

## Quick start

### 1. Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/download) installed

### 2. Clone and install

```bash
git clone https://github.com/scontractor/claude-alpha.git
cd claude-alpha
pip install -r requirements.txt
```

### 3. Configure (optional)

```bash
cp .env.example .env
```

Edit `.env` to change models, paths, or chunk settings. The defaults work out of the box.

### 4. Pull the AI model

```bash
ollama pull llama3.2:1b
```

> Using the 1B model for speed. Swap to `llama3.2` in `.env` for better quality at the cost of speed.

### 5. Run

```bash
streamlit run main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## How to use

### Uploading documents
1. Use the **Upload Documents** panel in the sidebar to drag and drop files
2. Click **Ingest Uploaded Files** — the app chunks and indexes them automatically
3. Alternatively, drop files into the `data/` folder and click **Scan & Ingest**

### Searching
- Go to the **Search** tab
- Type a query — results are ranked by semantic similarity, not just keyword match

### Asking questions
- Go to the **Ask** tab
- Type a question — the AI answers using only your documents
- Every answer shows **numbered citations** so you know exactly which document each claim comes from
- The conversation history persists within the session; click **Clear conversation** to reset

### Managing documents
- The **Documents** section in the sidebar lists everything ingested
- Click ✕ next to any document to remove it from the knowledge base

---

## Configuration

All settings can be overridden via `.env`:

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_MODEL` | `llama3.2:1b` | Ollama model for answering questions |
| `EMBED_MODEL` | `BAAI/bge-large-en-v1.5` | Embedding model for search |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `DATA_DIR` | `data` | Folder scanned by "Scan & Ingest" |
| `CHROMA_DIR` | `chroma_store` | Where the vector database is stored |
| `CHUNK_SIZE` | `512` | Characters per chunk |
| `CHUNK_OVERLAP` | `64` | Overlap between chunks |
| `TOP_K` | `5` | Number of results returned per query |

---

## Supported file types

| Format | Extension |
|---|---|
| PDF | `.pdf` |
| Word | `.docx` |
| Markdown | `.md`, `.markdown` |
| Plain text | `.txt` |

---

## Deployment

This app runs a Python server and **cannot** be hosted on GitHub Pages (which only serves static files).

### Option A — Streamlit Community Cloud (free)
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. **Note:** Ollama is a local service and won't be available in the cloud. You'll need to swap the LLM backend to a cloud API (e.g. Claude API or OpenAI) before deploying.

### Option B — Run locally and share via ngrok
```bash
# Install ngrok, then:
ngrok http 8501
```
This gives you a temporary public URL without changing any code.

### Option C — Self-host
Deploy to any Linux server (VPS, EC2, etc.) with Python and Ollama installed. Run `streamlit run main.py` behind a reverse proxy like Nginx.

---

## Tech stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| Vector database | ChromaDB (local) |
| Embeddings | `BAAI/bge-large-en-v1.5` via sentence-transformers |
| LLM | Ollama (local) |
| PDF parsing | pypdf |
| DOCX parsing | python-docx |
