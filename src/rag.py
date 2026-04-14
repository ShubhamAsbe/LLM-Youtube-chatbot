from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings

def vector_db():
    vector_store = Chroma(
        collection_name = "sample",
        embedding_function = embeddings,
        persist_directory="./db"
    )
    return vector_store

def chunking_text(video_transcript):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return text_splitter.split_text(video_transcript)
 
def embedding_chunks(chunk_text):
    embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")
    doc_results = embeddings.embed_documents(chunk_text)
    return doc_results