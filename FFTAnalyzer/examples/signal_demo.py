"""Signal-processing demonstration for the Week 12 FFTAnalyzer project."""

from pathlib import Path

from FFTAnalyzer.fft_analyzer.signal.analysis import (
    detect_peak_frequencies,
    dominant_frequency,
)
from FFTAnalyzer.fft_analyzer.signal.filters import (
    low_pass_filter,
)
from FFTAnalyzer.fft_analyzer.signal.generators import (
    multi_tone,
)
from FFTAnalyzer.fft_analyzer.visualization.plots import (
    plot_fft_spectrum,
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
    """Generate, analyze, filter, and visualize a sample signal."""
    sample_rate = 256.0
    duration = 2.0

    signal = multi_tone(
        [
            10.0,
            40.0,
        ],
        duration,
        sample_rate,
        amplitudes=[
            1.0,
            0.5,
        ],
    )

    peaks = detect_peak_frequencies(
        signal,
        sample_rate,
        count=2,
        min_frequency=1.0,
    )

    dominant = dominant_frequency(
        signal,
        sample_rate,
        min_frequency=1.0,
    )

    filtered = low_pass_filter(
        signal,
        sample_rate,
        cutoff=20.0,
    )

    filtered_dominant = dominant_frequency(
        filtered,
        sample_rate,
        min_frequency=1.0,
    )

    spectrum_path = (
        RESULTS_DIR
        / "signal_demo_spectrum.png"
    )

    comparison_path = (
        RESULTS_DIR
        / "signal_demo_comparison.png"
    )

    spectrogram_path = (
        RESULTS_DIR
        / "signal_demo_spectrogram.png"
    )

    plot_fft_spectrum(
        signal,
        sample_rate,
        title="Signal Demo Frequency Spectrum",
        save_path=spectrum_path,
    )

    plot_signal_comparison(
        signal,
        filtered,
        sample_rate=sample_rate,
        title="Original vs Low-Pass Filtered Signal",
        save_path=comparison_path,
    )

    plot_spectrogram(
        signal,
        sample_rate,
        window_size=128,
        hop_size=32,
        title="Signal Demo Spectrogram",
        save_path=spectrogram_path,
    )

    print(
        "Week 12 Signal Demo"
    )

    print(
        "-" * 60
    )

    print(
        f"Samples: {len(signal)}"
    )

    print(
        f"Sample rate: {sample_rate:.1f} Hz"
    )

    print(
        f"Detected peaks: {peaks}"
    )

    print(
        f"Dominant frequency: {dominant:.2f} Hz"
    )

    print(
        f"Filtered dominant frequency: "
        f"{filtered_dominant:.2f} Hz"
    )

    print()

    print(
        "Saved:"
    )

    print(
        spectrum_path
    )

    print(
        comparison_path
    )

    print(
        spectrogram_path
    )


if __name__ == "__main__":
    main()