import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from ..config import CHROMA_DB_DIR, EMBEDDING_MODEL

class LocalVectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vectorstore = Chroma(
            persist_directory=CHROMA_DB_DIR,
            embedding_function=self.embeddings
        )

    def ingest_document(self, file_path: str):
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
            
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)
        
        self.vectorstore.add_documents(documents=splits)
        print(f"Ingested {len(splits)} chunks from {file_path}")

    def as_retriever(self):
        return self.vectorstore.as_retriever()
