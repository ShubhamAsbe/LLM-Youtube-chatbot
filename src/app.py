import streamlit as st
from home import show_home
from main import show_main

if "page" not in st.session_state:
    st.session_state["page"] = "home"

if st.session_state["page"] == "home":
    show_home()
elif st.session_state["page"] == "main":
    show_main()