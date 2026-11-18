"""Audio-processing demonstration for the Week 12 FFTAnalyzer project."""

from pathlib import Path

from FFTAnalyzer.fft_analyzer.applications.audio_processor import (
    analyze_audio,
    filter_audio,
    save_wav,
)
from FFTAnalyzer.fft_analyzer.signal.generators import (
    multi_tone,
)
from FFTAnalyzer.fft_analyzer.visualization.plots import (
    plot_signal_comparison,
    plot_spectrogram,
)


PROJECT_ROOT = Path(
    __file__
).resolve().parent.parent

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def main() -> None:
    """Generate sample audio, filter it, analyze it, and save outputs."""
    sample_rate = 8000
    duration = 2.0

    audio = multi_tone(
        [
            440.0,
            1800.0,
        ],
        duration,
        sample_rate,
        amplitudes=[
            0.8,
            0.3,
        ],
    )

    filtered = filter_audio(
        audio,
        sample_rate,
        filter_type="low-pass",
        cutoff=1000.0,
    )

    original_analysis = analyze_audio(
        audio,
        sample_rate,
    )

    filtered_analysis = analyze_audio(
        filtered,
        sample_rate,
    )

    original_wav = (
        RESULTS_DIR
        / "audio_demo_original.wav"
    )

    filtered_wav = (
        RESULTS_DIR
        / "audio_demo_filtered.wav"
    )

    comparison_plot = (
        RESULTS_DIR
        / "audio_demo_comparison.png"
    )

    spectrogram_plot = (
        RESULTS_DIR
        / "audio_demo_spectrogram.png"
    )

    save_wav(
        original_wav,
        sample_rate,
        audio,
    )

    save_wav(
        filtered_wav,
        sample_rate,
        filtered,
    )

    plot_signal_comparison(
        audio,
        filtered,
        sample_rate=sample_rate,
        title="Original vs Low-Pass Filtered Audio",
        save_path=comparison_plot,
    )

    plot_spectrogram(
        filtered,
        sample_rate,
        window_size=256,
        hop_size=64,
        title="Filtered Audio Spectrogram",
        save_path=spectrogram_plot,
    )

    print(
        "Week 12 Audio Demo"
    )

    print(
        "-" * 60
    )

    print(
        "Original audio:"
    )

    for key, value in original_analysis.items():
        print(
            f"  {key}: {value:.4f}"
        )

    print()

    print(
        "Filtered audio:"
    )

    for key, value in filtered_analysis.items():
        print(
            f"  {key}: {value:.4f}"
        )

    print()

    print(
        "Saved:"
    )

    print(
        original_wav
    )

    print(
        filtered_wav
    )

    print(
        comparison_plot
    )

    print(
        spectrogram_plot
    )


if __name__ == "__main__":
    main()