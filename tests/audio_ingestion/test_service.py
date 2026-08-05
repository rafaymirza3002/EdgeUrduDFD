from __future__ import annotations

from io import BytesIO

import numpy as np
import pytest
import soundfile as sf

from urdu_deepfake.audio_ingestion.exceptions import AudioQualityError
from urdu_deepfake.audio_ingestion.models import AudioSource
from urdu_deepfake.audio_ingestion.service import AudioIngestionService


def test_upload_and_microphone_share_same_contract(
    clean_tone: np.ndarray,
    sample_rate: int,
) -> None:
    service = AudioIngestionService()

    wav = BytesIO()
    sf.write(wav, clean_tone, sample_rate, format="WAV", subtype="PCM_16")

    uploaded = service.from_upload(wav.getvalue(), filename="urdu.wav")
    captured = service.from_microphone_buffer(clean_tone, sample_rate=sample_rate)

    assert uploaded.source is AudioSource.UPLOAD
    assert captured.source is AudioSource.MICROPHONE
    assert uploaded.sample_rate == captured.sample_rate
    assert uploaded.quality.is_acceptable
    assert captured.quality.is_acceptable


def test_service_rejects_low_quality_by_default(sample_rate: int) -> None:
    service = AudioIngestionService()
    silent = np.zeros(sample_rate * 2, dtype=np.float32)

    with pytest.raises(AudioQualityError):
        service.from_microphone_buffer(silent, sample_rate=sample_rate)
