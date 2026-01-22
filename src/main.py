import streamlit as st
import random
import time
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage



st.title("Local LLM With UI")

client = ChatOllama(model="llama3.2:latest")

if "ollama_model" not in st.session_state:
    st.session_state["ollama_model"] = "llama3.2:latest"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

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
        
    # lc_messages=[]
    # for msg in st.session_state.messages:
    #     if msg["role"]=="user":
    #         lc_messages.append(HumanMessage(content=msg["content"]))
    #     else:
    #         lc_messages.append(AIMessage(content=msg["content"]))

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response=client.invoke(st.session_state.messages)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    st.markdown(response.content)