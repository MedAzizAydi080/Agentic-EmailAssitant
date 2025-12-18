import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag.vectorstore import LocalVectorStore
from src.config import DOCS_DIR

def ingest_data():
    store = LocalVectorStore()
    
    # We will assume UseCase1.txt is available and copy it to docs
    source_file = "/home/aziz/email-agent/UseCase1.txt"
    dest_path = os.path.join(DOCS_DIR, "rag_guide.txt")
    
    if os.path.exists(source_file):
        with open(source_file, "r") as f:
            content = f.read()
        with open(dest_path, "w") as f:
            f.write(content)
        print(f"Copied {source_file} to {dest_path}")
        
        store.ingest_document(dest_path)
    else:
        print(f"Source file {source_file} not found. Skipping ingestion.")

if __name__ == "__main__":
    ingest_data()
