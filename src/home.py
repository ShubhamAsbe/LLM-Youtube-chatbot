import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.extract_video_id import extract_youtube_video_id
from utils.generate_transcript import fetch_video_transcript,clean_transcript
from rag import chunking_text, embedding_chunks

def show_home():
    st.title("Home Page")
    st.write("Welcome to the Home Page of the Local LLM Chatbot application.")

    utube_video_url = st.text_input("Enter the Youtube URL, with Which you want to chat...")

    if utube_video_url:
        st.session_state["utube_url"] = utube_video_url

        video_id = extract_youtube_video_id(utube_video_url)

        if video_id:
            try:
                st.success(f"Extracted Video ID: {video_id}")
                st.session_state["video_id"] = video_id
                st.success("YouTube URL is valid. Proceeding the Video for chat interface...")
                video_transcript = fetch_video_transcript(video_id)
                cleaned_video_transcript = clean_transcript(video_transcript)
                st.session_state["video_transcript"] = cleaned_video_transcript
                chunk_text=chunking_text(cleaned_video_transcript)
                embedded_chunks = embedding_chunks(chunk_text)
                print("embedded_chunks:-",embedded_chunks)
            except Exception as e:                
                st.error(f"Error fetching transcript: {e}")
                return 
        else:
            st.error("Invalid YouTube URL. Please enter a valid URL.")
            return

        st.session_state["page"] = "main"
        st.rerun()
