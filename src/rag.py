from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import os
from langchain.schema import Document

DB_PATH = "../db/vectore_store"


def text_splitter(transcript, video_id):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    raw_chunks = splitter.split_text(transcript)

    documents = [
        Document(
            page_content=chunk,
            metadata={"video_id": video_id}
        )
        for chunk in raw_chunks
    ]

    return documents
    
# def vectorstore_creation(chunks):
#     # documents = [{"page_content": chunk} for chunk in chunks]
    
#     embedding_model = OllamaEmbeddings(model="mxbai-embed-large:latest", temperature=0.0)
#     vectorstore = FAISS.from_documents(chunks, embedding_model)
    
#     return vectorstore

def load_or_create_vectorstore():
    embedding_model = OllamaEmbeddings(model="mxbai-embed-large:latest", temperature=0.0)

    if os.path.exists(DB_PATH):
        print("📂 Loading existing FAISS DB")
        return FAISS.load_local(
            DB_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )

    print("🆕 Creating new FAISS DB")
    return FAISS.from_documents([], embedding_model)


def get_retriever(vector_store):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    return retriever

def get_prompt_template():
    return PromptTemplate(
        template="""
You are a helpful assistant.
Use the following context to answer the question.

Context:
{context}

Question:
{question}
""",
        input_variables=["context", "question"]
    )


def format_docs(retriever_docs):
    context_texts = "\n\n".join(doc.page_content for doc in retriever_docs)
    return context_texts


    
video_id = "Gfr50f6ZBvo"
transcript=document_ingestion(video_id)
chunks=text_splitter(transcript)
# print(chunks[0])
vector_store=vectorstore_creation(chunks)
# print(vector_store.index_to_docstore_id)
retriever=get_retriever(vector_store)
# print(retriever.invoke("what is deepmind"))
# question= "is the topic of nuclear fusion discussed in this video? if yes then what was discussed"
# context= retriever.invoke(question)
# context_texts = "\n\n".join(doc.page_content for doc in context)
prompt = get_prompt_template()


llm=ChatOllama(model="llama3.2:latest", temperature=0.5)

parser = StrOutputParser()

# chain = prompt | llm

# response = chain.invoke({
#     "context": context_texts,
#     "question": question
# })

# print("Response:", response)

parallel_chain=RunnableParallel({
    'context':retriever | RunnableLambda(format_docs),
    'question':RunnablePassthrough()
})

main_chain = parallel_chain | prompt | llm | parser

# parallel_chain.invoke('who is Demis')

response=main_chain.invoke('Can you summarize the video')

print("Response:", response)