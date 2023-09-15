from app import  init_app
init_app()
import streamlit as st
import hashlib
from audio_recorder_streamlit import audio_recorder
from utils import get_assembly_ai_transcriber, get_weaviate_client, get_unsplash_image_with_keyword, get_keywords_to_search, get_title_of_note
from tempfile import NamedTemporaryFile
from streamlit_elements import elements, sync, event, mui

wv_client = get_weaviate_client()
transcriber = get_assembly_ai_transcriber()

if "audio_hash" not in st.session_state:
    st.session_state["audio_hash"] = None

if "audio_transcript" not in st.session_state:
    st.session_state["audio_transcript"] = ""

st.title("VoiceMyNote 🗣️🗒️")

a, b = st.columns([2, 4])

with a:
    record_or_upload = st.radio("record or upload", options=[
        "record",
        "upload"
    ])

audio_bytes = None
if record_or_upload == "record":
    with b:
        audio_bytes = audio_recorder("record your thoughts!",
                                     icon_size="2x"
                                     )
else:
    with b:
        uploaded_file = st.file_uploader("upload_audio", type=".wav")
        if uploaded_file:
            audio_bytes = uploaded_file

if audio_bytes:
    audio_hash = hashlib.sha256(audio_bytes).hexdigest()

    if existing_hash := st.session_state.get("audio_hash", None) != audio_hash:
        st.session_state["audio_hash"] = audio_hash

        with NamedTemporaryFile("w+b", suffix=audio_hash) as audio_file:
            audio_file.write(audio_bytes)

            with st.spinner("transcribing..."):
                transcript = transcriber.transcribe(str(audio_file.name))
                st.session_state["audio_transcript"] = transcript.text

    st.audio(audio_bytes, format="audio/wav")

text_note = st.text_area("Edit Transcribed Note or Write your own!",
                         value=st.session_state.audio_transcript).strip()

if text_note and st.button("save note"):
    title = get_title_of_note(text_note)
    keyword = get_keywords_to_search(text_note)
    image = get_unsplash_image_with_keyword(keyword)
    with elements("my_elements"):
        with mui.Card(key="key",
                      sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
                      elevation=1):
            mui.CardHeader(
                title=title,
            )
            mui.CardMedia(
                component="img",
                image=image,
            )

            with mui.CardContent(sx={"flex": 1}):
                mui.Typography(text_note)

    with st.spinner("indexing..."):
        wv_client.data_object.create(data_object={
            "title": title,
            "image": image,
            "note": text_note,
        },
            class_name=st.secrets.weaviate.index_class,
        )
