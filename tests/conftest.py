from __future__ import annotations

import numpy as np
import pytest


@pytest.fixture
def sample_rate() -> int:
    return 16_000


@pytest.fixture
def clean_tone(sample_rate: int) -> np.ndarray:
    duration = 2.0
    time = np.arange(int(sample_rate * duration), dtype=np.float32) / sample_rate
    return (0.2 * np.sin(2 * np.pi * 440 * time)).astype(np.float32)
