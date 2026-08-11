from __future__ import annotations

from dataclasses import asdict

import streamlit as st

from urdu_deepfake.audio_ingestion import AudioIngestionService
from urdu_deepfake.audio_ingestion.exceptions import AudioIngestionError

st.set_page_config(
    page_title="Urdu Deepfake Audio Detector",
    page_icon="🎙️",
    layout="centered",
)

st.title("Urdu Deepfake Audio Detector")

st.caption(
    "Module 2 prototype: local dual-mode audio ingestion "
    "and quality assurance"
)


service = AudioIngestionService()


record_tab, upload_tab = st.tabs(
    [
        "Record live voice",
        "Upload recording",
    ]
)


with record_tab:
    recorded_audio = st.audio_input(
        "Record a short Urdu voice sample"
    )

    if recorded_audio is not None:
        try:
            audio_bytes = recorded_audio.getvalue()

            item = service.from_microphone_file(
                audio_bytes,
                filename=recorded_audio.name or "microphone.wav",
            )

            st.audio(audio_bytes)

            st.success("Microphone recording accepted.")

            duration_seconds = (
                len(item.samples) / item.sample_rate
            )

            st.subheader("Audio information")

            st.write(
                "**Source:**",
                item.source.value,
            )

            st.write(
                "**Sample rate:**",
                f"{item.sample_rate:,} Hz",
            )

            st.write(
                "**Duration:**",
                f"{duration_seconds:.2f} seconds",
            )

            st.write(
                "**Original format:**",
                item.original_format,
            )

            st.write(
                "**Original name:**",
                item.original_name,
            )

            st.write(
                "**Waveform shape:**",
                str(item.samples.shape),
            )

            st.write(
                "**Waveform dtype:**",
                str(item.samples.dtype),
            )

            st.subheader("Quality report")

            st.json(asdict(item.quality))

        except AudioIngestionError as exc:
            st.error(
                f"Microphone recording rejected: {exc}"
            )


with upload_tab:
    uploaded_audio = st.file_uploader(
        "Choose an existing Urdu recording",
        type=["wav", "mp3", "flac"],
    )

    if uploaded_audio is not None:
        try:
            audio_bytes = uploaded_audio.getvalue()

            item = service.from_upload(
                audio_bytes,
                filename=uploaded_audio.name,
            )

            st.audio(audio_bytes)

            st.success("Uploaded recording accepted.")

            duration_seconds = (
                len(item.samples) / item.sample_rate
            )

            st.subheader("Audio information")

            st.write(
                "**Source:**",
                item.source.value,
            )

            st.write(
                "**Sample rate:**",
                f"{item.sample_rate:,} Hz",
            )

            st.write(
                "**Duration:**",
                f"{duration_seconds:.2f} seconds",
            )

            st.write(
                "**Original format:**",
                item.original_format,
            )

            st.write(
                "**Original name:**",
                item.original_name,
            )

            st.write(
                "**Waveform shape:**",
                str(item.samples.shape),
            )

            st.write(
                "**Waveform dtype:**",
                str(item.samples.dtype),
            )

            st.subheader("Quality report")

            st.json(asdict(item.quality))

        except AudioIngestionError as exc:
            st.error(
                f"Uploaded recording rejected: {exc}"
            )