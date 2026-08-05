from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from .config import IngestionConfig
from .models import QualityReport


def _as_channel_last(samples: NDArray[np.float32]) -> NDArray[np.float32]:
    if samples.ndim == 1:
        return samples[:, None]
    if samples.ndim == 2:
        return samples
    raise ValueError("Audio must be one-dimensional or channel-last two-dimensional.")


def assess_quality(
    samples: NDArray[np.float32],
    sample_rate: int,
    config: IngestionConfig,
) -> QualityReport:
    """Calculate deterministic, model-independent quality indicators."""

    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive.")
    if samples.size == 0:
        raise ValueError("Audio contains no samples.")
    if not np.isfinite(samples).all():
        raise ValueError("Audio contains NaN or infinite values.")

    channel_last = _as_channel_last(samples)
    duration = channel_last.shape[0] / sample_rate
    channels = channel_last.shape[1]

    absolute = np.abs(channel_last)
    peak = float(np.max(absolute))
    rms = float(np.sqrt(np.mean(np.square(channel_last, dtype=np.float64))))
    silence_ratio = float(np.mean(absolute < config.silence_amplitude_threshold))
    clipping_ratio = float(np.mean(absolute >= config.clipping_amplitude_threshold))

    reasons: list[str] = []
    if duration < config.min_duration_seconds:
        reasons.append("Audio is shorter than the minimum supported duration.")
    if duration > config.max_duration_seconds:
        reasons.append("Audio is longer than the maximum supported duration.")
    if silence_ratio > config.max_silence_ratio:
        reasons.append("Audio contains too much silence or very low energy.")
    if clipping_ratio > config.max_clipping_ratio:
        reasons.append("Audio contains excessive clipping.")

    return QualityReport(
        duration_seconds=duration,
        sample_rate=sample_rate,
        channels=channels,
        peak_amplitude=peak,
        rms_amplitude=rms,
        silence_ratio=silence_ratio,
        clipping_ratio=clipping_ratio,
        is_acceptable=not reasons,
        rejection_reasons=tuple(reasons),
    )
