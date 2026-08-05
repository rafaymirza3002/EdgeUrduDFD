from _thread import LockType
from dataclasses import dataclass, field
from threading import Event, Lock

import numpy as np
import sounddevice as sd

from .exceptions import MicrophoneError


@dataclass(slots=True)
class MicrophoneRecorder:
    """Stateful local recorder for CLI/desktop/edge use."""

    sample_rate: int = 16_000
    channels: int = 1
    dtype: str = "float32"

    _frames: list[np.ndarray] = field(
        default_factory=list,
        init=False,
        repr=False,
    )
    _stream: sd.InputStream | None = field(
        default=None,
        init=False,
        repr=False,
    )
    _lock: LockType = field(
        default_factory=Lock,
        init=False,
        repr=False,
    )
    _recording: Event = field(
        default_factory=Event,
        init=False,
        repr=False,
    )

    @property
    def is_recording(self) -> bool:
        return self._recording.is_set()

    def start(self) -> None:
        if self.is_recording:
            raise MicrophoneError("Recording is already active.")

        self._frames.clear()

        def callback(
            indata: np.ndarray,
            frames: int,
            time_info: object,
            status: sd.CallbackFlags,
        ) -> None:
            del frames, time_info
            if status:
                # Callback warnings are intentionally non-fatal; the final quality
                # report decides whether the recording is usable.
                pass

            with self._lock:
                self._frames.append(indata.copy())

        try:
            self._stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=self.dtype,
                callback=callback,
            )
            self._stream.start()
            self._recording.set()

        except (sd.PortAudioError, OSError) as exc:
            self._stream = None
            raise MicrophoneError(
                "Unable to start microphone capture."
            ) from exc

    def stop(self) -> np.ndarray:
        if not self.is_recording or self._stream is None:
            raise MicrophoneError("No active recording to stop.")

        try:
            self._stream.stop()
            self._stream.close()

        except (sd.PortAudioError, OSError) as exc:
            raise MicrophoneError(
                "Unable to stop microphone capture cleanly."
            ) from exc

        finally:
            self._stream = None
            self._recording.clear()

        with self._lock:
            if not self._frames:
                raise MicrophoneError(
                    "Microphone produced no audio frames."
                )

            samples = np.concatenate(
                self._frames,
                axis=0,
            ).astype(np.float32, copy=False)

        return samples[:, 0] if self.channels == 1 else samples

    def cancel(self) -> None:
        if self._stream is not None:
            try:
                self._stream.abort()
                self._stream.close()

            finally:
                self._stream = None

        self._recording.clear()

        with self._lock:
            self._frames.clear()