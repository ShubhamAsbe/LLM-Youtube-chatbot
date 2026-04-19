from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage, SystemMessage
from src.core.config import OLLAMA_MODEL

class LLMService:
    def __init__(self, model: str = OLLAMA_MODEL):
        self.model = ChatOllama(model=model)
    
    def stream_response(self, prompt: str):
        return self.model.stream([SystemMessage(content="You are a helpful assistant"),HumanMessage(content=prompt)])
    
    @staticmethod
    def build_prompt(query: str, context: str, chat_history: str) -> str:
        return f"""
        You are an AI assistant specialized in answering questions about a video.

        ### Instructions:
        - Use ONLY the provided CONTEXT to answer the question.
        - Use CHAT HISTORY only to understand the conversation flow and resolve references (e.g., "this", "that", follow-ups).
        - Do NOT rely on prior knowledge outside the given CONTEXT.
        - If the answer is not explicitly present in the CONTEXT, respond exactly with:
        "Your question is out of context please ask the valid question".

        ### Response Rules:
        - Be precise and concise.
        - Do not hallucinate or assume information.
        - Do not repeat the question.
        - Do not mention "context" or "chat history" in your answer.

        ---

        ### CHAT HISTORY:
        {chat_history}
        ---
        ### CONTEXT:
        {context}
        ---
        ### QUESTION:
        {query}
        ---
        ### ANSWER:
        """