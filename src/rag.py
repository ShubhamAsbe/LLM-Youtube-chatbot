from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name = "sample",
    embedding_function = embeddings,
    persist_directory="./db"
)