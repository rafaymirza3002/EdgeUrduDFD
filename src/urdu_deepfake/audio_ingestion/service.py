from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

import numpy as np
from numpy.typing import NDArray

from .config import IngestionConfig
from .exceptions import AudioQualityError
from .file_loader import decode_audio
from .models import AudioInput, AudioSource
from .quality import assess_quality


class AudioIngestionService:
    """Application-facing facade for all supported audio input paths."""

    def __init__(
        self,
        config: IngestionConfig | None = None,
    ) -> None:
        """Create the service with audio-quality configuration."""

        self.config = config or IngestionConfig()

    def from_upload(
        self,
        source: str | Path | bytes | BinaryIO,
        *,
        filename: str,
        reject_low_quality: bool = True,
    ) -> AudioInput:
        """Create an AudioInput from an uploaded audio file."""

        samples, sample_rate, original_format = decode_audio(
            source,
            filename=filename,
        )

        return self._build(
            samples=samples,
            sample_rate=sample_rate,
            source=AudioSource.UPLOAD,
            original_name=filename,
            original_format=original_format,
            reject_low_quality=reject_low_quality,
        )

    def from_microphone_file(
        self,
        source: bytes | BinaryIO,
        *,
        filename: str = "microphone.wav",
        reject_low_quality: bool = True,
    ) -> AudioInput:
        """Create an AudioInput from browser-recorded microphone audio."""

        samples, sample_rate, original_format = decode_audio(
            source,
            filename=filename,
        )

        return self._build(
            samples=samples,
            sample_rate=sample_rate,
            source=AudioSource.MICROPHONE,
            original_name=None,
            original_format=original_format,
            reject_low_quality=reject_low_quality,
        )

    def from_microphone_buffer(
        self,
        samples: NDArray[np.float32],
        *,
        sample_rate: int,
        reject_low_quality: bool = True,
    ) -> AudioInput:
        """Create an AudioInput from a raw microphone sample buffer."""

        return self._build(
            samples=np.asarray(
                samples,
                dtype=np.float32,
            ),
            sample_rate=sample_rate,
            source=AudioSource.MICROPHONE,
            original_name=None,
            original_format="raw-float32",
            reject_low_quality=reject_low_quality,
        )

    def _build(
        self,
        *,
        samples: NDArray[np.float32],
        sample_rate: int,
        source: AudioSource,
        original_name: str | None,
        original_format: str,
        reject_low_quality: bool,
    ) -> AudioInput:
        """Validate audio and build the common AudioInput interface."""

        quality = assess_quality(
            samples,
            sample_rate,
            self.config,
        )

        if reject_low_quality and not quality.is_acceptable:
            raise AudioQualityError(
                " ".join(quality.rejection_reasons)
            )

        return AudioInput(
            samples=samples,
            sample_rate=sample_rate,
            source=source,
            original_name=original_name,
            original_format=original_format,
            quality=quality,
        )