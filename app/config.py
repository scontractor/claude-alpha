import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", "chroma_store"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "knowledge_base")

EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-large-en-v1.5")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "64"))
EMBED_BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "32"))
TOP_K = int(os.getenv("TOP_K", "5"))

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".md", ".txt", ".markdown"}

# BGE retrieval query prefix (required for correct retrieval quality)
BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "
