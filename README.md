# LLM YouTube Chatbot

A LangChain-based GenAI application for chatting with YouTube video transcripts using local LLM (Ollama).

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Install Ollama and pull models:

```bash
ollama pull llama3.2:latest
ollama pull nomic-embed-text
```

3. Run the application:

```bash
streamlit run app.py
```

## Features

- Extract transcripts from YouTube videos
- Create vector embeddings using ChromaDB
- Chat with video content using local LLM
- RAG-based question answering
