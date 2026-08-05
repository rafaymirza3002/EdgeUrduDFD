from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IngestionConfig:
    """Validation and quality thresholds for Module 2."""

    min_duration_seconds: float = 1.0
    max_duration_seconds: float = 30.0
    silence_amplitude_threshold: float = 0.01
    max_silence_ratio: float = 0.80
    clipping_amplitude_threshold: float = 0.999
    max_clipping_ratio: float = 0.01
    target_recording_sample_rate: int = 16_000
    recording_channels: int = 1

    def __post_init__(self) -> None:
        if self.min_duration_seconds <= 0:
            raise ValueError("min_duration_seconds must be positive.")
        if self.max_duration_seconds <= self.min_duration_seconds:
            raise ValueError("max_duration_seconds must exceed min_duration_seconds.")
        if not 0 <= self.max_silence_ratio <= 1:
            raise ValueError("max_silence_ratio must be between 0 and 1.")
        if not 0 <= self.max_clipping_ratio <= 1:
            raise ValueError("max_clipping_ratio must be between 0 and 1.")
        if self.target_recording_sample_rate <= 0:
            raise ValueError("target_recording_sample_rate must be positive.")
