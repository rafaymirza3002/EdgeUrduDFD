from __future__ import annotations

import numpy as np

from urdu_deepfake.audio_ingestion.config import IngestionConfig
from urdu_deepfake.audio_ingestion.quality import assess_quality


def test_clean_audio_is_accepted(clean_tone: np.ndarray, sample_rate: int) -> None:
    report = assess_quality(clean_tone, sample_rate, IngestionConfig())

    assert report.is_acceptable
    assert report.duration_seconds == 2.0
    assert report.channels == 1
    assert report.rejection_reasons == ()


def test_silent_audio_is_rejected(sample_rate: int) -> None:
    samples = np.zeros(sample_rate * 2, dtype=np.float32)
    report = assess_quality(samples, sample_rate, IngestionConfig())

    assert not report.is_acceptable
    assert report.silence_ratio == 1.0
    assert any("silence" in reason.lower() for reason in report.rejection_reasons)


def test_heavily_clipped_audio_is_rejected(sample_rate: int) -> None:
    samples = np.ones(sample_rate * 2, dtype=np.float32)
    report = assess_quality(samples, sample_rate, IngestionConfig())

    assert not report.is_acceptable
    assert report.clipping_ratio == 1.0
