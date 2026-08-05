from __future__ import annotations

import streamlit as st

from urdu_deepfake.audio_ingestion import AudioIngestionService
from urdu_deepfake.audio_ingestion.exceptions import AudioIngestionError

st.set_page_config(page_title="Urdu Deepfake Detector", page_icon="🎙️")
st.title("Urdu Deepfake Audio Detector")
st.caption("Module 2 prototype: local dual-mode audio ingestion and quality assurance")

service = AudioIngestionService()

tab_mic, tab_upload = st.tabs(["Record live voice", "Upload recording"])

with tab_mic:
    recorded = st.audio_input("Record a short Urdu voice sample")
    if recorded is not None:
        st.audio(recorded)
        try:
            item = service.from_upload(
                recorded.getvalue(),
                filename=recorded.name or "microphone.wav",
            )
            st.success("Microphone recording accepted.")
            st.json(item.quality.__dict__)
        except AudioIngestionError as exc:
            st.error(str(exc))

with tab_upload:
    uploaded = st.file_uploader(
        "Choose an existing Urdu recording",
        type=["wav", "mp3", "flac"],
        accept_multiple_files=False,
    )
    if uploaded is not None:
        st.audio(uploaded)
        try:
            item = service.from_upload(
                uploaded.getvalue(),
                filename=uploaded.name,
            )
            st.success("Uploaded recording accepted.")
            st.json(item.quality.__dict__)
        except AudioIngestionError as exc:
            st.error(str(exc))

st.info(
    "This module performs acquisition and quality checks only. "
    "Resampling, mono conversion, trimming, normalization, and segmentation belong to Module 3."
)
