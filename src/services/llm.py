from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from src.core.config import OLLAMA_MODEL

class LLMService:
    def __init__(self, model: str = OLLAMA_MODEL):
        self.model = ChatOllama(model=model)
    
    def stream_response(self, prompt: str):
        return self.model.stream([HumanMessage(content=prompt)])
    
    @staticmethod
    def build_prompt(query: str, context: str) -> str:
        return f"""
        You are a helpful assistant.
        Answer ONLY from the provided context. If user ask summarize the video then 
        summarize video.
        If answer is not available, say "Not available in video".

        Context:
        {context}

        Question:
        {query}

        Answer:
        """
