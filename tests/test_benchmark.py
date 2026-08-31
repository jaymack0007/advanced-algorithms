"""Tests for benchmark utilities."""

import pytest

from src.sorting.basic_sorts import insertion_sort
from src.utils.benchmark import AlgorithmBenchmark


def test_generate_supported_data_types():
    benchmark = AlgorithmBenchmark(warmup_runs=0)
    data_types = [
        "random",
        "sorted",
        "reverse",
        "duplicates",
        "single_value",
        "nearly_sorted",
        "mountain",
        "valley",
    ]

    for data_type in data_types:
        result = benchmark.generate_test_data(11, data_type, seed=42)
        assert len(result) == 11


def test_generate_data_is_reproducible():
    benchmark = AlgorithmBenchmark(warmup_runs=0)
    first = benchmark.generate_test_data(20, "random", seed=42)
    second = benchmark.generate_test_data(20, "random", seed=42)
    assert first == second


def test_invalid_data_type_raises_error():
    benchmark = AlgorithmBenchmark(warmup_runs=0)
    with pytest.raises(ValueError):
        benchmark.generate_test_data(10, "not_a_type")


def test_time_algorithm_records_result():
    benchmark = AlgorithmBenchmark(warmup_runs=0)
    data = benchmark.generate_test_data(25, "random", seed=42)
    result = benchmark.time_algorithm(
        insertion_sort,
        data,
        runs=2,
        data_type="random",
    )

    assert result.algorithm_name == "insertion_sort"
    assert result.input_size == 25
    assert result.average_time >= 0
    assert len(benchmark.results) == 1
