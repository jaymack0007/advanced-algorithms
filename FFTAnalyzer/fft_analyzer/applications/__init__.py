"""Application-level processing tools for FFTAnalyzer."""

from .audio_processor import (
    analyze_audio,
    audio_spectrogram,
    filter_audio,
    load_wav,
    process_wav,
    save_wav,
)
from .data_analyzer import (
    analyze_time_series,
    autocorrelation,
    dominant_period,
    moving_average,
    periodic_frequencies,
    seasonality_strength,
)
from .image_processor import (
    apply_image_filter,
    compress_image_array,
    compress_image_file,
    frequency_magnitude,
    load_image,
    process_image_file,
    save_image,
)


__all__ = [
    "analyze_audio",
    "analyze_time_series",
    "apply_image_filter",
    "audio_spectrogram",
    "autocorrelation",
    "compress_image_array",
    "compress_image_file",
    "dominant_period",
    "filter_audio",
    "frequency_magnitude",
    "load_image",
    "load_wav",
    "moving_average",
    "periodic_frequencies",
    "process_image_file",
    "process_wav",
    "save_image",
    "save_wav",
    "seasonality_strength",
]