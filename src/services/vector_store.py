from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from src.core.config import (
    DB_PATH, EMBEDDING_MODEL, COLLECTION_NAME, 
    CHUNK_SIZE, CHUNK_OVERLAP, SEPARATORS
)

class VectorStoreService:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=SEPARATORS
        )
    
    def create_embeddings(self, text: str) -> str:
        chunks = self.text_splitter.split_text(text)
        docs = [Document(page_content=chunk) for chunk in chunks]
        Chroma.from_documents(
            documents=docs,
            collection_name=COLLECTION_NAME,
            embedding=self.embeddings,
            persist_directory=str(DB_PATH)
        )
        return "Embeddings stored successfully!"
    
    def get_retriever(self, k: int = 3):
        db = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=str(DB_PATH),
            embedding_function=self.embeddings
        )
        return db.as_retriever(search_kwargs={"k": k})
