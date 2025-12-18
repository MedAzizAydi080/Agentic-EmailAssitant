import os

# Configuration for Local Models (Ollama)
OLLAMA_BASE_URL = "http://localhost:11434"
LLM_MODEL = "llama3" # Make sure to run `ollama pull llama3`
EMBEDDING_MODEL = "all-MiniLM-L6-v2" # SentenceTransformers local model

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MEMORY_DB_PATH = os.path.join(DATA_DIR, "memory", "episodes.db")
PROMPTS_DIR = os.path.join(DATA_DIR, "prompts")
DOCS_DIR = os.path.join(DATA_DIR, "docs")
CHROMA_DB_DIR = os.path.join(DATA_DIR, "chroma_db")

# Ensure dirs exist
for d in [DATA_DIR, os.path.dirname(MEMORY_DB_PATH), PROMPTS_DIR, DOCS_DIR, CHROMA_DB_DIR]:
    os.makedirs(d, exist_ok=True)
