from __future__ import annotations

from io import BytesIO

import numpy as np
import pytest
import soundfile as sf

from urdu_deepfake.audio_ingestion.exceptions import (
    CorruptAudioError,
    UnsupportedAudioFormatError,
)
from urdu_deepfake.audio_ingestion.file_loader import decode_audio


def test_decodes_valid_wav(clean_tone: np.ndarray, sample_rate: int) -> None:
    buffer = BytesIO()
    sf.write(buffer, clean_tone, sample_rate, format="WAV", subtype="PCM_16")
    payload = buffer.getvalue()

    samples, decoded_rate, original_format = decode_audio(
        payload,
        filename="sample.wav",
    )

    assert decoded_rate == sample_rate
    assert original_format == "wav"
    assert samples.dtype == np.float32
    assert samples.shape == clean_tone.shape


def test_rejects_unsupported_extension() -> None:
    with pytest.raises(UnsupportedAudioFormatError):
        decode_audio(b"not audio", filename="sample.txt")


def test_rejects_corrupt_supported_file() -> None:
    with pytest.raises(CorruptAudioError):
        decode_audio(b"not a real wave file", filename="broken.wav")
