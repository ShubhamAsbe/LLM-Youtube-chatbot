import streamlit as st
import random
import time
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage

def show_main():
    st.title("Local LLM With UI")
    
    if st.button("⬅ Back to Home"):
        st.session_state["page"] = "home"
        st.rerun()
    
    @st.cache_resource
    def load_model():
        return ChatOllama(model="llama3.2:latest")

    client = load_model()

    if "ollama_model" not in st.session_state:
        st.session_state["ollama_model"] = "llama3.2:latest"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Optionally show the YouTube URL if present
    utube_url = st.session_state.get("utube_url", None)
    if utube_url:
        st.info(f"YouTube URL: {utube_url}")

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = client.invoke(st.session_state.messages)
            st.markdown(response.content)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.content})
        