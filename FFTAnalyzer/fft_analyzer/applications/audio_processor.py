"""Audio processing workflows for the Week 12 FFTAnalyzer project."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io import wavfile

from FFTAnalyzer.fft_analyzer.signal.analysis import (
    dominant_frequency,
    spectrogram,
)
from FFTAnalyzer.fft_analyzer.signal.filters import (
    band_pass_filter,
    high_pass_filter,
    low_pass_filter,
)


def _as_audio(values) -> np.ndarray:
    """Convert audio input to a one-dimensional floating-point signal."""
    try:
        audio = np.asarray(
            values,
            dtype=float,
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "Audio must contain numeric values."
        ) from exc

    if audio.ndim != 1:
        raise ValueError(
            "Audio must be mono and one-dimensional."
        )

    if audio.size == 0:
        raise ValueError(
            "Audio cannot be empty."
        )

    if not np.all(
        np.isfinite(audio)
    ):
        raise ValueError(
            "Audio must contain finite values."
        )

    return audio.copy()


def _normalize_integer_audio(
    values: np.ndarray,
) -> np.ndarray:
    """Convert integer PCM audio into floating-point values near [-1, 1]."""
    if np.issubdtype(
        values.dtype,
        np.integer,
    ):
        info = np.iinfo(
            values.dtype
        )

        scale = max(
            abs(
                info.min
            ),
            abs(
                info.max
            ),
        )

        return (
            values.astype(
                float
            )
            / scale
        )

    return values.astype(
        float
    )


def load_wav(
    path,
) -> tuple[int, np.ndarray]:
    """
    Load a WAV file.

    Integer PCM data is normalized to floating point first. Stereo files
    are then converted to mono by averaging the normalized channels.
    """
    file_path = Path(
        path
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"WAV file not found: {file_path}"
        )

    sample_rate, data = wavfile.read(
        file_path
    )

    normalized = _normalize_integer_audio(
        np.asarray(
            data
        )
    )

    if normalized.ndim == 2:
        audio = np.mean(
            normalized,
            axis=1,
        )

    elif normalized.ndim == 1:
        audio = normalized

    else:
        raise ValueError(
            "Unsupported WAV channel layout."
        )

    return (
        int(
            sample_rate
        ),
        np.asarray(
            audio,
            dtype=float,
        ),
    )


def save_wav(
    path,
    sample_rate: int,
    values,
) -> None:
    """
    Save floating-point audio as 16-bit PCM WAV.

    Values are clipped to [-1, 1] before conversion.
    """
    audio = _as_audio(
        values
    )

    if not isinstance(
        sample_rate,
        int,
    ):
        raise TypeError(
            "sample_rate must be an integer."
        )

    if sample_rate <= 0:
        raise ValueError(
            "sample_rate must be positive."
        )

    clipped = np.clip(
        audio,
        -1.0,
        1.0,
    )

    pcm = np.rint(
        clipped
        * 32767.0
    ).astype(
        np.int16
    )

    wavfile.write(
        Path(
            path
        ),
        sample_rate,
        pcm,
    )


def filter_audio(
    values,
    sample_rate: float,
    *,
    filter_type: str,
    cutoff: float | None = None,
    low_cutoff: float | None = None,
    high_cutoff: float | None = None,
) -> np.ndarray:
    """Apply a supported FFT-based filter to audio data."""
    audio = _as_audio(
        values
    )

    normalized = str(
        filter_type
    ).lower()

    if normalized in {
        "low",
        "lowpass",
        "low-pass",
    }:
        if cutoff is None:
            raise ValueError(
                "cutoff is required for a low-pass filter."
            )

        return low_pass_filter(
            audio,
            sample_rate,
            cutoff,
        )

    if normalized in {
        "high",
        "highpass",
        "high-pass",
    }:
        if cutoff is None:
            raise ValueError(
                "cutoff is required for a high-pass filter."
            )

        return high_pass_filter(
            audio,
            sample_rate,
            cutoff,
        )

    if normalized in {
        "band",
        "bandpass",
        "band-pass",
    }:
        if (
            low_cutoff is None
            or high_cutoff is None
        ):
            raise ValueError(
                "low_cutoff and high_cutoff are required "
                "for a band-pass filter."
            )

        return band_pass_filter(
            audio,
            sample_rate,
            low_cutoff,
            high_cutoff,
        )

    raise ValueError(
        "filter_type must be low-pass, high-pass, or band-pass."
    )


def audio_spectrogram(
    values,
    sample_rate: float,
    *,
    window_size: int = 256,
    hop_size: int | None = None,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """Compute a spectrogram for mono audio."""
    audio = _as_audio(
        values
    )

    return spectrogram(
        audio,
        sample_rate,
        window_size=window_size,
        hop_size=hop_size,
    )


def analyze_audio(
    values,
    sample_rate: float,
) -> dict[str, float]:
    """Return basic audio statistics and dominant frequency."""
    audio = _as_audio(
        values
    )

    peak = float(
        np.max(
            np.abs(
                audio
            )
        )
    )

    rms = float(
        np.sqrt(
            np.mean(
                audio
                * audio
            )
        )
    )

    frequency = dominant_frequency(
        audio,
        sample_rate,
        min_frequency=1.0,
    )

    return {
        "duration_seconds": float(
            audio.size
            / sample_rate
        ),
        "peak_amplitude": peak,
        "rms_amplitude": rms,
        "dominant_frequency": float(
            frequency
        ),
    }


def process_wav(
    input_path,
    output_path,
    *,
    filter_type: str,
    cutoff: float | None = None,
    low_cutoff: float | None = None,
    high_cutoff: float | None = None,
) -> dict[str, object]:
    """
    Load a WAV file, apply an FFT filter, and save the filtered result.
    """
    sample_rate, audio = load_wav(
        input_path
    )

    filtered = filter_audio(
        audio,
        sample_rate,
        filter_type=filter_type,
        cutoff=cutoff,
        low_cutoff=low_cutoff,
        high_cutoff=high_cutoff,
    )

    peak = float(
        np.max(
            np.abs(
                filtered
            )
        )
    )

    if peak > 1.0:
        filtered = (
            filtered
            / peak
        )

    save_wav(
        output_path,
        sample_rate,
        filtered,
    )

    return {
        "sample_rate": sample_rate,
        "input_samples": int(
            audio.size
        ),
        "output_samples": int(
            filtered.size
        ),
        "output_path": str(
            output_path
        ),
    }