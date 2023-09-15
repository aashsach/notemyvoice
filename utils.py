import streamlit as st
import assemblyai as aai
import weaviate
import requests
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import HumanMessage
from constants import TITLE_OF_NOTE_PROMPT, KEYWORD_OF_NOTE_PROMPT
import os





@st.cache_data
def get_open_ai_key() -> str:
    return st.secrets.openai.api_key


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
    if wv_client.schema.exists(st.secrets.weaviate.index_class):
        # wv_client.schema.delete_class("VoiceNote")
        pass
    else:
        voice_ny_notes_class = {
            "class": st.secrets.weaviate.index_class,
            "vectorizer": "text2vec-openai",
            "properties": [
                {
                    "name": "title",
                    "dataType": "text",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": True,
                        }

                    }
                },
                {
                    "name": "note",
                    "dataType": ["text"],
                },
                {
                    "name": "image",
                    "dataType": "text",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": True,
                        }
                    }
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


@st.cache_resource
def get_langchain_openai_client():
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = st.secrets.langsmith.api_key
    os.environ["LANGCHAIN_PROJECT"] = "voicemynote"
    llm = ChatOpenAI(openai_api_key=get_open_ai_key())
    return llm


@st.cache_data(max_entries=1024)
def get_unsplash_image_with_keyword(keyword: str) -> str:
    image_link = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8Mnx8YWJzdHJhY3R8ZW58MHx8fHwxNjk0NzkzNTg4fDA&ixlib=rb-4.0.3&q=80&w=200"
    try:
        response = requests.get(
            f"https://api.unsplash.com/search/photos?client_id={st.secrets.unsplash.access_key}&query={keyword}"
        ).json()
        image_link = response["results"][0]["urls"]["thumb"]
    except:
        try:
            response = requests.get(
                f"https://api.unsplash.com/photos/random/?client_id={st.secrets.unsplash.access_key}"
            ).json()

            image_link = response["urls"]["thumb"]
        except:
            pass
    finally:
        return image_link


def get_title_of_note(note):
    llm = get_langchain_openai_client()
    ai_message = llm(messages=[HumanMessage(content=TITLE_OF_NOTE_PROMPT.format(note=note))])
    return ai_message.content


def get_keywords_to_search(note):
    llm = get_langchain_openai_client()
    ai_message = llm(messages=[HumanMessage(content=KEYWORD_OF_NOTE_PROMPT.format(note=note))])
    return ai_message.content
