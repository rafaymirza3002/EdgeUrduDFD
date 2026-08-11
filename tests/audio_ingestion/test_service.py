from __future__ import annotations

from io import BytesIO

import numpy as np
import soundfile as sf

from urdu_deepfake.audio_ingestion import AudioIngestionService
from urdu_deepfake.audio_ingestion.models import AudioSource


def make_valid_wav_bytes() -> bytes:
    """Create a valid 2-second WAV file entirely in memory."""

    sample_rate = 16_000
    duration_seconds = 2.0
    frequency_hz = 440.0

    t = np.linspace(
        0.0,
        duration_seconds,
        int(sample_rate * duration_seconds),
        endpoint=False,
    )

    samples = (
        0.2 * np.sin(2.0 * np.pi * frequency_hz * t)
    ).astype(np.float32)

    buffer = BytesIO()

    sf.write(
        buffer,
        samples,
        sample_rate,
        format="WAV",
        subtype="PCM_16",
    )

    return buffer.getvalue()


def test_microphone_file_preserves_source() -> None:
    """Browser microphone audio must remain labeled as microphone input."""

    service = AudioIngestionService()
    wav_bytes = make_valid_wav_bytes()

    result = service.from_microphone_file(
        wav_bytes,
        filename="microphone.wav",
    )

    assert result.source is AudioSource.MICROPHONE
    assert result.original_name is None
    assert result.original_format == "wav"
    assert result.sample_rate == 16_000
    assert result.samples.size > 0


def test_upload_preserves_source() -> None:
    """Uploaded audio must remain labeled as uploaded input."""

    service = AudioIngestionService()
    wav_bytes = make_valid_wav_bytes()

    result = service.from_upload(
        wav_bytes,
        filename="sample.wav",
    )

    assert result.source is AudioSource.UPLOAD
    assert result.original_name == "sample.wav"
    assert result.original_format == "wav"
    assert result.sample_rate == 16_000
    assert result.samples.size > 0
