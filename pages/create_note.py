import streamlit as st
import hashlib
from audio_recorder_streamlit import audio_recorder
from utils.utils import get_assembly_ai_transcriber, get_weaviate_client
from tempfile import NamedTemporaryFile

st.set_page_config(page_title="VoiceMyNote", page_icon="🗒️", initial_sidebar_state="collapsed")

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
    st.write(f"Storing thought to DB: {text_note}")
    with st.spinner("indexing..."):
        wv_client.data_object.create(data_object={
            "note": text_note,
        },
            class_name="VoiceNote"
        )
