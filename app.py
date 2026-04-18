import streamlit as st
from src.ui import home_page, chat_page

st.set_page_config(
    page_title="YouTube Chatbot",
    page_icon="🤖",
    layout="centered"
)

if "page" not in st.session_state:
    st.session_state["page"] = "home"

if st.session_state["page"] == "home":
    home_page.render()
elif st.session_state["page"] == "chat":
    chat_page.render()
