from __future__ import annotations

from dataclasses import asdict
from typing import Any

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
    "Module 2 prototype: local dual-mode audio ingestion and quality assurance"
)

service = AudioIngestionService()


def display_audio_result(item: Any, success_message: str) -> None:
    """Display the standardized AudioInput result returned by Module 2."""

    st.success(success_message)

    duration_seconds = len(item.samples) / item.sample_rate

    st.subheader("Audio information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Sample rate", f"{item.sample_rate:,} Hz")
        st.metric("Duration", f"{duration_seconds:.2f} seconds")

    with col2:
        source_value = getattr(item.source, "value", str(item.source))

        st.metric("Source", source_value)
        st.metric("Format", item.original_format.upper())

    if item.original_name is not None:
        st.write("**Original name:**", item.original_name)
    else:
        st.write("**Original name:** Browser microphone recording")

    st.write("**Waveform shape:**", str(item.samples.shape))
    st.write("**Waveform data type:**", str(item.samples.dtype))

    st.subheader("Quality report")

    # QualityReport is a slotted dataclass, so it does not have __dict__.
    # asdict() safely converts it into a dictionary for Streamlit.
    st.json(asdict(item.quality))


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
            item = service.from_bytes(
                recorded_audio.getvalue(),
                original_name=getattr(
                    recorded_audio,
                    "name",
                    "microphone_recording.wav",
                ),
                source="microphone",
            )

            st.audio(recorded_audio.getvalue())

            display_audio_result(
                item,
                "Microphone recording accepted.",
            )

        except AudioIngestionError as exc:
            st.error(str(exc))

        except Exception as exc:
            st.exception(exc)


with upload_tab:
    uploaded_audio = st.file_uploader(
        "Choose an existing Urdu recording",
        type=["wav", "mp3", "flac"],
    )

    if uploaded_audio is not None:
        try:
            audio_bytes = uploaded_audio.getvalue()

            item = service.from_bytes(
                audio_bytes,
                original_name=uploaded_audio.name,
                source="file",
            )

            st.audio(audio_bytes)

            display_audio_result(
                item,
                "Uploaded recording accepted.",
            )

        except AudioIngestionError as exc:
            st.error(str(exc))

        except Exception as exc:
            st.exception(exc)