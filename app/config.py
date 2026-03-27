from pathlib import Path

DATA_DIR = Path("data")
CHROMA_DIR = Path("chroma_store")
COLLECTION_NAME = "knowledge_base"

EMBED_MODEL = "BAAI/bge-large-en-v1.5"
OLLAMA_MODEL = "llama3.2"
OLLAMA_BASE_URL = "http://localhost:11434"

CHUNK_SIZE = 512        # characters
CHUNK_OVERLAP = 64      # characters
EMBED_BATCH_SIZE = 32
TOP_K = 5

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".md", ".txt", ".markdown"}

# BGE retrieval query prefix (required for correct retrieval quality)
BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "
