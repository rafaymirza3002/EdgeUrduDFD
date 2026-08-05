from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import BinaryIO

import numpy as np
import soundfile as sf

from .exceptions import CorruptAudioError, UnsupportedAudioFormatError

SUPPORTED_EXTENSIONS = {".wav", ".flac", ".mp3"}


def _validate_extension(filename: str) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise UnsupportedAudioFormatError(
            f"Unsupported format '{extension or '<none>'}'. Supported: {supported}."
        )
    return extension.lstrip(".")


def decode_audio(
    source: str | Path | bytes | BinaryIO,
    *,
    filename: str,
) -> tuple[np.ndarray, int, str]:
    """
    Decode an uploaded/path-based recording.

    The extension is an early UX check; successful decoding is the real validity check.
    Audio is returned as float32 with shape (frames,) or (frames, channels).
    """

    original_format = _validate_extension(filename)
    readable: str | Path | BinaryIO

    if isinstance(source, bytes):
        readable = BytesIO(source)
    else:
        readable = source

    try:
        samples, sample_rate = sf.read(
            readable,
            dtype="float32",
            always_2d=False,
        )
    except (sf.LibsndfileError, RuntimeError, OSError, ValueError) as exc:
        raise CorruptAudioError(f"Unable to decode '{filename}'.") from exc

    samples = np.asarray(samples, dtype=np.float32)
    if samples.size == 0:
        raise CorruptAudioError(f"'{filename}' contains no audio frames.")
    if samples.ndim not in (1, 2):
        raise CorruptAudioError(f"'{filename}' has an unsupported channel layout.")

    return samples, int(sample_rate), original_format
