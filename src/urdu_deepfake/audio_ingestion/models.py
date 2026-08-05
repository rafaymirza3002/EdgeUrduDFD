from dataclasses import dataclass
from enum import StrEnum

import numpy as np
from numpy.typing import NDArray

FloatAudio = NDArray[np.float32]


class AudioSource(StrEnum):
    MICROPHONE = "microphone"
    UPLOAD = "upload"


@dataclass(frozen=True, slots=True)
class QualityReport:
    duration_seconds: float
    sample_rate: int
    channels: int
    peak_amplitude: float
    rms_amplitude: float
    silence_ratio: float
    clipping_ratio: float
    is_acceptable: bool
    rejection_reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AudioInput:
    """Stable hand-off object from Module 2 to Module 3."""

    samples: FloatAudio
    sample_rate: int
    source: AudioSource
    original_name: str | None
    original_format: str
    quality: QualityReport

    def __post_init__(self) -> None:
        if self.samples.dtype != np.float32:
            raise TypeError("samples must use float32.")
        if self.samples.ndim not in (1, 2):
            raise ValueError("samples must be mono or channel-last 2D audio.")
        if self.sample_rate <= 0:
            raise ValueError("sample_rate must be positive.")
