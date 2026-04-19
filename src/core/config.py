from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "db"

# Model configurations
OLLAMA_MODEL = "llama3.2:latest"
EMBEDDING_MODEL = "nomic-embed-text:latest"

# Vector DB settings
COLLECTION_NAME = "sample"
RETRIEVER_K = 3

# Text splitting settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
SEPARATORS = ["\n\n", "\n", ".", " ", ""]
