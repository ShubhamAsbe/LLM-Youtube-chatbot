import streamlit as st

def show_home():
	st.title("Home Page")
	st.write("Welcome to the Home Page of the Local LLM Chatbot application.")
	utube_video_url = st.text_input("Enter the Utube URL, with Which you want to chat...")
	if utube_video_url:
		st.session_state["utube_url"] = utube_video_url
		st.session_state["page"] = "main"
		st.rerun()
