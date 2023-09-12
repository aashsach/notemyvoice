import streamlit as st
from utils import  get_weaviate_client

wv_client = get_weaviate_client()

concept_to_search = st.text_input("search something").strip()
if concept_to_search and st.button("search"):
    response = wv_client.query.get(
        class_name='VoiceNote',
        properties=["note"],
    ).with_near_text(content={
        "concepts": [concept_to_search]
    }).with_additional(["distance"]).do()

    st.write(response)