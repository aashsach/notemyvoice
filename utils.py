import streamlit as st
import assemblyai as aai
import weaviate

st.set_page_config(page_title="VoiceMyNote", page_icon="🗒️", initial_sidebar_state="collapsed")

with st.expander("api key configuration"):
    open_ai_key = st.text_input("OpenAI key", type="password")
    assemblyai_api_key = st.text_input("AssemblyAI key", type="password")
    weaviate_url = st.text_input("Weaviate URL", type="default")
    weaviate_api_key = st.text_input("Weaviate URL", type="password")


@st.cache_data
def get_open_ai_key() -> str:
    return open_ai_key or st.secrets.openai.api_key


@st.cache_resource
def get_assembly_ai_transcriber():
    aai.settings.api_key = st.secrets.assemblyai.api_key
    return aai.Transcriber()


@st.cache_resource
def get_weaviate_client():
    auth_config = weaviate.AuthApiKey(api_key=st.secrets.weaviate.api_key)
    wv_client = weaviate.Client(
        url=st.secrets.weaviate.url,
        auth_client_secret=auth_config,
        additional_headers={
            "X-OpenAI-Api-Key": get_open_ai_key()
        }
    )
    if wv_client.schema.exists("VoiceNote"):
        # wv_client.schema.delete_class("VoiceNote")
        pass
    else:
        voice_ny_notes_class = {
            "class": "VoiceNote",
            "vectorizer": "text2vec-openai",
            "properties": [
                {
                    "name": "note",
                    "dataType": ["text"]
                }
            ],
            "moduleConfig": {
                "text2vec-openai": {
                    "vectorizeClassName": False,
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text"
                },
                "generative-openai": {
                }
            }
        }
        wv_client.schema.create_class(voice_ny_notes_class)
    return wv_client
