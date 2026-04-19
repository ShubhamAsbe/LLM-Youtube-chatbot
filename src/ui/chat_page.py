import streamlit as st
from src.services.llm import LLMService
from src.services.vector_store import VectorStoreService
from langchain.messages import HumanMessage, AIMessage

def render():
    st.title("Chat with Video")
    
    if st.button("⬅ Back to Home"):
        st.session_state["page"] = "home"
        st.session_state["messages"] = []
        st.rerun()
    
    @st.cache_resource
    def load_services():
        return LLMService(), VectorStoreService()

    llm_service, vector_service = load_services()

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "lc_messages" not in st.session_state:
        st.session_state.lc_messages = []

    if url := st.session_state.get("utube_url"):
        st.info(f"📺 {url}")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the video..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.lc_messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)
        video_id = st.session_state.get("video_id")
        retriever = vector_service.get_retriever(video_id=video_id)
        docs = retriever.invoke(prompt)
        context = "\n\n".join([doc.page_content for doc in docs]) if docs else "No relevant context found."
        chat_history = "\n".join([
            f"User: {msg.content}" if msg.type == "human" else f"Assistant: {msg.content}"
            for msg in st.session_state.lc_messages
        ])
        final_prompt = LLMService.build_prompt(prompt, context, chat_history)
        
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            for chunk in llm_service.stream_response(final_prompt):
                if chunk.content:
                    full_response += chunk.content
                    response_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.lc_messages.append(AIMessage(content=full_response))
