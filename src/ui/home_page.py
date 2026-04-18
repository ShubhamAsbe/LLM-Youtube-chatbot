import streamlit as st
from src.core.youtube import extract_video_id, fetch_transcript
from src.services.vector_store import VectorStoreService

def render():
    st.title("YouTube Video Chatbot")
    st.write("Enter a YouTube URL to start chatting with the video content.")

    url = st.text_input("YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

    if url:
        st.session_state["utube_url"] = url
        video_id = extract_video_id(url)

        if video_id:
            try:
                st.success(f"Video ID: {video_id}")
                st.session_state["video_id"] = video_id
                
                with st.spinner("Fetching transcript..."):
                    transcript = fetch_transcript(video_id)
                    st.session_state["video_transcript"] = transcript
                
                with st.spinner("Creating embeddings..."):
                    vector_service = VectorStoreService()
                    msg = vector_service.create_embeddings(transcript)
                    st.success(msg)
                
                st.session_state["page"] = "chat"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Invalid YouTube URL. Please check and try again.")
