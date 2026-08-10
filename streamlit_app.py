from __future__ import annotations

from dataclasses import asdict
<<<<<<< Updated upstream
from typing import Any
=======
>>>>>>> Stashed changes

import streamlit as st

from urdu_deepfake.audio_ingestion import AudioIngestionService
from urdu_deepfake.audio_ingestion.exceptions import AudioIngestionError


<<<<<<< Updated upstream
=======
# ---------------------------------------------------------
# Streamlit page configuration
# ---------------------------------------------------------

>>>>>>> Stashed changes
st.set_page_config(
    page_title="Urdu Deepfake Audio Detector",
    page_icon="🎙️",
    layout="centered",
)

<<<<<<< Updated upstream
st.title("Urdu Deepfake Audio Detector")
st.caption(
    "Module 2 prototype: local dual-mode audio ingestion and quality assurance"
)
=======

# ---------------------------------------------------------
# Page heading
# ---------------------------------------------------------

st.title("Urdu Deepfake Audio Detector")

st.caption(
    "Module 2 prototype: local dual-mode audio ingestion "
    "and quality assurance"
)


# ---------------------------------------------------------
# Audio ingestion service
# ---------------------------------------------------------
>>>>>>> Stashed changes

service = AudioIngestionService()


<<<<<<< Updated upstream
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

=======
# ---------------------------------------------------------
# Input tabs
# ---------------------------------------------------------
>>>>>>> Stashed changes

record_tab, upload_tab = st.tabs(
    [
        "Record live voice",
        "Upload recording",
    ]
)


<<<<<<< Updated upstream
=======
# =========================================================
# TAB 1: RECORD LIVE VOICE
# =========================================================

>>>>>>> Stashed changes
with record_tab:
    recorded_audio = st.audio_input(
        "Record a short Urdu voice sample"
    )

    if recorded_audio is not None:
        try:
<<<<<<< Updated upstream
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

=======
            # Read the browser recording directly as bytes.
            audio_bytes = recorded_audio.getvalue()

            # Send the bytes to Module 2.
            item = service.ingest_bytes(
                audio_bytes,
                filename="microphone.wav",
                source="microphone",
            )

            # Allow the user to replay the captured recording.
            st.audio(audio_bytes)

            # Inform the user that Module 2 accepted the sample.
            st.success("Microphone recording accepted.")

            # Display standardized AudioInput information.
            st.subheader("Audio information")

            duration_seconds = (
                len(item.samples) / item.sample_rate
            )

            st.write(
                f"**Sample rate:** {item.sample_rate:,} Hz"
            )

            st.write(
                f"**Duration:** {duration_seconds:.2f} seconds"
            )

            st.write(
                f"**Source:** "
                f"{getattr(item.source, 'value', item.source)}"
            )

            st.write(
                f"**Original format:** "
                f"{item.original_format.upper()}"
            )

            if item.original_name is not None:
                st.write(
                    f"**Original name:** {item.original_name}"
                )

            st.write(
                f"**Waveform shape:** {item.samples.shape}"
            )

            st.write(
                f"**Waveform dtype:** {item.samples.dtype}"
            )

            # QualityReport is a slotted dataclass.
            # Use asdict() instead of __dict__.
            st.subheader("Quality report")
            st.json(asdict(item.quality))

        except AudioIngestionError as exc:
            st.error(f"Audio rejected: {exc}")

>>>>>>> Stashed changes
        except Exception as exc:
            st.exception(exc)


<<<<<<< Updated upstream
=======
# =========================================================
# TAB 2: UPLOAD EXISTING AUDIO FILE
# =========================================================

>>>>>>> Stashed changes
with upload_tab:
    uploaded_audio = st.file_uploader(
        "Choose an existing Urdu recording",
        type=["wav", "mp3", "flac"],
    )
<<<<<<< Updated upstream

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

=======

    if uploaded_audio is not None:
        try:
            # Read the uploaded file directly into memory.
            # The recording is not intentionally saved
            # permanently to the project folder.
            audio_bytes = uploaded_audio.getvalue()

            # Send the uploaded bytes to Module 2.
            item = service.ingest_bytes(
                audio_bytes,
                filename=uploaded_audio.name,
                source="file",
            )

            # Let the user replay the uploaded audio.
            st.audio(audio_bytes)

            # Inform the user that processing succeeded.
            st.success("Uploaded recording accepted.")

            # Display standardized AudioInput information.
            st.subheader("Audio information")

            duration_seconds = (
                len(item.samples) / item.sample_rate
            )

            st.write(
                f"**Sample rate:** {item.sample_rate:,} Hz"
            )

            st.write(
                f"**Duration:** {duration_seconds:.2f} seconds"
            )

            st.write(
                f"**Source:** "
                f"{getattr(item.source, 'value', item.source)}"
            )

            st.write(
                f"**Original format:** "
                f"{item.original_format.upper()}"
            )

            if item.original_name is not None:
                st.write(
                    f"**Original name:** {item.original_name}"
                )

            st.write(
                f"**Waveform shape:** {item.samples.shape}"
            )

            st.write(
                f"**Waveform dtype:** {item.samples.dtype}"
            )

            # Correct way to convert the slotted
            # QualityReport dataclass into a dictionary.
            st.subheader("Quality report")
            st.json(asdict(item.quality))

        except AudioIngestionError as exc:
            st.error(f"Audio rejected: {exc}")

>>>>>>> Stashed changes
        except Exception as exc:
            st.exception(exc)