import streamlit as st


def init_app():
    st.set_page_config(page_title="VoiceMyNote", page_icon="🗒️")

    with st.expander("api key configuration"):
        open_ai_key = st.text_input("OpenAI key", type="password")
        assemblyai_api_key = st.text_input("AssemblyAI key", type="password")
        weaviate_url = st.text_input("Weaviate URL", type="default")
        weaviate_api_key = st.text_input("Weaviate URL", type="password")


init_app()


@st.cache_data
def get_readme():
    with open("./README.md") as f:
        readme = f.read()
    return readme


st.markdown(body=get_readme())
