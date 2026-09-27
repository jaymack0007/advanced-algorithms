"""Timing and memory utilities for Week 5 benchmarks."""

import time
import tracemalloc
from typing import Any, Callable, Dict


def measure_function(
    function: Callable,
    *args: Any,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Measure execution time and peak memory usage.

    Returns the function result, elapsed time in seconds,
    and peak memory usage in bytes.
    """
    tracemalloc.start()

    start = time.perf_counter()

    result = function(
        *args,
        **kwargs,
    )

    elapsed = time.perf_counter() - start

    _, peak_memory = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    return {
        "result": result,
        "time_seconds": elapsed,
        "memory_bytes": peak_memory,
    }


def average_time(
    function: Callable,
    *args: Any,
    repetitions: int = 3,
    **kwargs: Any,
) -> float:
    """
    Return average execution time across repeated runs.
    """
    times = []

    for _ in range(repetitions):
        start = time.perf_counter()

        function(
            *args,
            **kwargs,
        )

        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return sum(times) / len(times)