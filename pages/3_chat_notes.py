from app import init_app
init_app()
from utils import get_llama_weaviate_vector_store
import streamlit as st


chat_engine = get_llama_weaviate_vector_store().as_chat_engine()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.spinner("looking up your notes..."):
        response = chat_engine.query(prompt)
        msg = response.response
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)