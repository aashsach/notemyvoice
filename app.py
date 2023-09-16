import streamlit as st
from types import SimpleNamespace


def init_app():
    st.set_page_config(page_title="VoiceMyNote", page_icon="🗒️")

    st.title("VoiceMyNote 🗣️🗒️")

    if "api_keys" not in st.session_state:
        st.session_state["api_keys"] = SimpleNamespace(
            openai_api_key="",
            assemblyai_api_key="",
            weaviate_url="",
            weaviate_api_key="",
            unsplash_access_key=""
        )

    with st.expander("api key configuration", expanded=True):
        openai_api_key = st.text_input("OpenAI key", type="password",
                                       value=st.session_state.api_keys.openai_api_key)
        assemblyai_api_key = st.text_input("AssemblyAI key", type="password",
                                           value=st.session_state.api_keys.assemblyai_api_key)
        # weaviate_url = st.text_input("Weaviate URL", type="default",
        #                              value=st.session_state.api_keys.weaviate_url)
        # weaviate_api_key = st.text_input("Weaviate api_key", type="password",
        #                                  value=st.session_state.api_keys.weaviate_api_key)
        # unsplash_api_key = st.text_input("Unsplash API Key", type="password",
        #                                  value=st.session_state.api_keys.unsplash_api_key)

        if openai_api_key:
            st.session_state.api_keys.openai_api_key = openai_api_key
        if assemblyai_api_key:
            st.session_state.api_keys.assemblyai_api_key = assemblyai_api_key

        if not st.session_state.api_keys.openai_api_key:
            st.error("open ai is mandatory")
            st.stop()
        # if weaviate_url:
        #     st.session_state.api_keys.weaviate_url = weaviate_url
        # if weaviate_api_key:
        #     st.session_state.api_keys.weaviate_api_key = weaviate_api_key
        # if unsplash_api_key:
        #     st.session_state.api_keys.unsplash_api_key = unsplash_api_key


init_app()


@st.cache_data
def get_readme():
    with open("./README.md") as f:
        readme = f.read()
    return readme


st.markdown(body=get_readme())
