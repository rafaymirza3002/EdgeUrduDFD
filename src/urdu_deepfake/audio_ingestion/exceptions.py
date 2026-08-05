class AudioIngestionError(Exception):
    """Base exception for audio ingestion failures."""


class UnsupportedAudioFormatError(AudioIngestionError):
    """Raised when the supplied format is not supported."""


class CorruptAudioError(AudioIngestionError):
    """Raised when audio cannot be decoded safely."""


class AudioQualityError(AudioIngestionError):
    """Raised when decoded audio fails mandatory quality checks."""


class MicrophoneError(AudioIngestionError):
    """Raised when microphone capture cannot be completed."""
