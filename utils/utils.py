import streamlit as st
import assemblyai as aai
import weaviate
from weaviate.embedded import EmbeddedOptions


@st.cache_resource
def get_assembly_ai_transcriber():
    aai.settings.api_key = st.secrets.assemblyai.api_key
    return aai.Transcriber()


@st.cache_resource
def get_weaviate_client():
    wv_client = weaviate.Client(
        embedded_options=EmbeddedOptions(),
        additional_headers={
            "X-OpenAI-Api-Key": st.secrets.openai.api_key
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
