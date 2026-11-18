"""Signal generators for the Week 12 FFTAnalyzer project."""

from __future__ import annotations

import math

import numpy as np


DEFAULT_SAMPLE_RATE = 44_100.0


def _validate_sample_rate(
    sample_rate: float,
) -> float:
    """Validate and return a positive sampling rate."""
    try:
        sample_rate = float(
            sample_rate
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "sample_rate must be numeric."
        ) from exc

    if (
        not math.isfinite(
            sample_rate
        )
        or sample_rate <= 0
    ):
        raise ValueError(
            "sample_rate must be positive and finite."
        )

    return sample_rate


def _validate_duration(
    duration: float,
) -> float:
    """Validate and return a positive signal duration."""
    try:
        duration = float(
            duration
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "duration must be numeric."
        ) from exc

    if (
        not math.isfinite(
            duration
        )
        or duration <= 0
    ):
        raise ValueError(
            "duration must be positive and finite."
        )

    return duration


def _validate_amplitude(
    amplitude: float,
) -> float:
    """Validate a nonnegative finite amplitude."""
    try:
        amplitude = float(
            amplitude
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "amplitude must be numeric."
        ) from exc

    if (
        not math.isfinite(
            amplitude
        )
        or amplitude < 0
    ):
        raise ValueError(
            "amplitude must be nonnegative and finite."
        )

    return amplitude


def _validate_frequency(
    frequency: float,
    sample_rate: float,
    *,
    name: str = "frequency",
) -> float:
    """Validate a frequency below the Nyquist limit."""
    try:
        frequency = float(
            frequency
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            f"{name} must be numeric."
        ) from exc

    if (
        not math.isfinite(
            frequency
        )
        or frequency < 0
    ):
        raise ValueError(
            f"{name} must be nonnegative and finite."
        )

    nyquist = (
        sample_rate
        / 2.0
    )

    if frequency > nyquist:
        raise ValueError(
            f"{name} cannot exceed the Nyquist frequency."
        )

    return frequency


def sample_count(
    duration: float,
    sample_rate: float = DEFAULT_SAMPLE_RATE,
) -> int:
    """Return the number of samples for a duration and sampling rate."""
    duration = _validate_duration(
        duration
    )

    sample_rate = _validate_sample_rate(
        sample_rate
    )

    count = int(
        round(
            duration
            * sample_rate
        )
    )

    if count <= 0:
        raise ValueError(
            "duration and sample_rate produce no samples."
        )

    return count


def time_axis(
    duration: float,
    sample_rate: float = DEFAULT_SAMPLE_RATE,
) -> np.ndarray:
    """
    Return sample times beginning at zero.

    The endpoint is excluded so adjacent samples are separated by
    exactly 1 / sample_rate seconds.
    """
    rate = _validate_sample_rate(
        sample_rate
    )

    count = sample_count(
        duration,
        rate,
    )

    return (
        np.arange(
            count,
            dtype=float,
        )
        / rate
    )


def sine_wave(
    frequency: float,
    duration: float,
    sample_rate: float = DEFAULT_SAMPLE_RATE,
    *,
    amplitude: float = 1.0,
    phase: float = 0.0,
) -> np.ndarray:
    """Generate a sampled sine wave."""
    rate = _validate_sample_rate(
        sample_rate
    )

    frequency = _validate_frequency(
        frequency,
        rate,
    )

    amplitude = _validate_amplitude(
        amplitude
    )

    try:
        phase = float(
            phase
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "phase must be numeric."
        ) from exc

    if not math.isfinite(
        phase
    ):
        raise ValueError(
            "phase must be finite."
        )

    times = time_axis(
        duration,
        rate,
    )

    return (
        amplitude
        * np.sin(
            2.0
            * np.pi
            * frequency
            * times
            + phase
        )
    )


def multi_tone(
    frequencies,
    duration: float,
    sample_rate: float = DEFAULT_SAMPLE_RATE,
    *,
    amplitudes=None,
    phases=None,
) -> np.ndarray:
    """
    Generate a signal containing multiple sinusoidal frequencies.

    When amplitudes or phases are omitted, every tone uses amplitude
    1.0 and phase 0.0.
    """
    rate = _validate_sample_rate(
        sample_rate
    )

    try:
        frequency_values = list(
            frequencies
        )
    except TypeError as exc:
        raise TypeError(
            "frequencies must be an iterable."
        ) from exc

    if not frequency_values:
        raise ValueError(
            "At least one frequency is required."
        )

    validated_frequencies = [
        _validate_frequency(
            frequency,
            rate,
        )
        for frequency in frequency_values
    ]

    tone_count = len(
        validated_frequencies
    )

    if amplitudes is None:
        amplitude_values = [
            1.0
        ] * tone_count
    else:
        try:
            amplitude_values = list(
                amplitudes
            )
        except TypeError as exc:
            raise TypeError(
                "amplitudes must be an iterable."
            ) from exc

        if len(
            amplitude_values
        ) != tone_count:
            raise ValueError(
                "amplitudes must match the number of frequencies."
            )

        amplitude_values = [
            _validate_amplitude(
                amplitude
            )
            for amplitude in amplitude_values
        ]

    if phases is None:
        phase_values = [
            0.0
        ] * tone_count
    else:
        try:
            phase_values = [
                float(value)
                for value in phases
            ]
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise TypeError(
                "phases must contain numeric values."
            ) from exc

        if len(
            phase_values
        ) != tone_count:
            raise ValueError(
                "phases must match the number of frequencies."
            )

        if not all(
            math.isfinite(
                value
            )
            for value in phase_values
        ):
            raise ValueError(
                "phases must contain finite values."
            )

    times = time_axis(
        duration,
        rate,
    )

    signal = np.zeros(
        times.size,
        dtype=float,
    )

    for (
        frequency,
        amplitude,
        phase,
    ) in zip(
        validated_frequencies,
        amplitude_values,
        phase_values,
    ):
        signal += (
            amplitude
            * np.sin(
                2.0
                * np.pi
                * frequency
                * times
                + phase
            )
        )

    return signal


def chirp_signal(
    start_frequency: float,
    end_frequency: float,
    duration: float,
    sample_rate: float = DEFAULT_SAMPLE_RATE,
    *,
    amplitude: float = 1.0,
    phase: float = 0.0,
) -> np.ndarray:
    """
    Generate a linear-frequency chirp.

    The instantaneous frequency changes linearly from start_frequency
    to end_frequency over the requested duration.
    """
    rate = _validate_sample_rate(
        sample_rate
    )

    duration = _validate_duration(
        duration
    )

    start_frequency = (
        _validate_frequency(
            start_frequency,
            rate,
            name="start_frequency",
        )
    )

    end_frequency = (
        _validate_frequency(
            end_frequency,
            rate,
            name="end_frequency",
        )
    )

    amplitude = _validate_amplitude(
        amplitude
    )

    try:
        phase = float(
            phase
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "phase must be numeric."
        ) from exc

    if not math.isfinite(
        phase
    ):
        raise ValueError(
            "phase must be finite."
        )

    times = time_axis(
        duration,
        rate,
    )

    sweep_rate = (
        end_frequency
        - start_frequency
    ) / duration

    instantaneous_phase = (
        2.0
        * np.pi
        * (
            start_frequency
            * times
            + 0.5
            * sweep_rate
            * times
            * times
        )
        + phase
    )

    return (
        amplitude
        * np.sin(
            instantaneous_phase
        )
    )


def white_noise(
    duration: float,
    sample_rate: float = DEFAULT_SAMPLE_RATE,
    *,
    amplitude: float = 1.0,
    seed: int | None = None,
) -> np.ndarray:
    """
    Generate zero-mean Gaussian white noise.

    amplitude controls the target standard deviation.
    """
    amplitude = _validate_amplitude(
        amplitude
    )

    count = sample_count(
        duration,
        sample_rate,
    )

    rng = np.random.default_rng(
        seed
    )

    if amplitude == 0:
        return np.zeros(
            count,
            dtype=float,
        )

    return rng.normal(
        loc=0.0,
        scale=amplitude,
        size=count,
    )


def pink_noise(
    duration: float,
    sample_rate: float = DEFAULT_SAMPLE_RATE,
    *,
    amplitude: float = 1.0,
    seed: int | None = None,
    rows: int = 16,
) -> np.ndarray:
    """
    Generate approximate pink noise with a Voss-McCartney-style method.

    Pink noise contains more low-frequency energy than white noise.
    Multiple random sources are updated at different rates and summed,
    giving an approximate 1/f spectrum without relying on numpy.fft.

    amplitude controls the final standard deviation.
    """
    amplitude = _validate_amplitude(
        amplitude
    )

    count = sample_count(
        duration,
        sample_rate,
    )

    if not isinstance(
        rows,
        int,
    ):
        raise TypeError(
            "rows must be an integer."
        )

    if rows <= 0:
        raise ValueError(
            "rows must be positive."
        )

    rng = np.random.default_rng(
        seed
    )

    if amplitude == 0:
        return np.zeros(
            count,
            dtype=float,
        )

    output = np.zeros(
        count,
        dtype=float,
    )

    for row in range(
        rows
    ):
        block_size = (
            1
            << row
        )

        block_count = int(
            math.ceil(
                count
                / block_size
            )
        )

        values = rng.normal(
            size=block_count
        )

        expanded = np.repeat(
            values,
            block_size,
        )

        output += expanded[
            :count
        ]

    output -= np.mean(
        output
    )

    standard_deviation = float(
        np.std(
            output
        )
    )

    if standard_deviation > 0:
        output *= (
            amplitude
            / standard_deviation
        )

    return output