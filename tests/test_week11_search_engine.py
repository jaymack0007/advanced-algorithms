"""Tests for the unified Week 11 StringSearchEngine."""

import pytest

from StringSearchEngine.core.search_engine import (
    SUPPORTED_METHODS,
    SearchResult,
    StringSearchEngine,
)


def test_supported_methods():
    assert SUPPORTED_METHODS == (
        "kmp",
        "rk",
        "sa",
        "tree",
    )


def test_engine_stores_text():
    engine = StringSearchEngine(
        "banana"
    )

    assert engine.text == "banana"


def test_indexes_are_lazy():
    engine = StringSearchEngine(
        "banana"
    )

    assert engine._suffix_array_index is None
    assert engine._suffix_tree is None


def test_kmp_does_not_build_indexes():
    engine = StringSearchEngine(
        "banana"
    )

    engine.find(
        "ana",
        method="kmp",
    )

    assert engine._suffix_array_index is None
    assert engine._suffix_tree is None


def test_kmp_search():
    engine = StringSearchEngine(
        "banana"
    )

    result = engine.find(
        "ana",
        method="kmp",
    )

    assert result.positions == [
        1,
        3,
    ]


def test_rabin_karp_search():
    engine = StringSearchEngine(
        "banana"
    )

    result = engine.find(
        "ana",
        method="rk",
    )

    assert result.positions == [
        1,
        3,
    ]


def test_suffix_array_search():
    engine = StringSearchEngine(
        "banana"
    )

    result = engine.find(
        "ana",
        method="sa",
    )

    assert result.positions == [
        1,
        3,
    ]

    assert engine._suffix_array_index is not None


def test_suffix_tree_search():
    engine = StringSearchEngine(
        "banana"
    )

    result = engine.find(
        "ana",
        method="tree",
    )

    assert result.positions == [
        1,
        3,
    ]

    assert engine._suffix_tree is not None


def test_all_methods_agree():
    engine = StringSearchEngine(
        "ABCABCABC"
    )

    results = engine.find_all(
        "ABC"
    )

    positions = {
        tuple(
            result.positions
        )
        for result in results.values()
    }

    assert positions == {
        (
            0,
            3,
            6,
        )
    }


def test_result_object():
    engine = StringSearchEngine(
        "banana"
    )

    result = engine.find(
        "ana"
    )

    assert isinstance(
        result,
        SearchResult,
    )


def test_result_count():
    engine = StringSearchEngine(
        "AAAAA"
    )

    result = engine.find(
        "AAA",
        method="kmp",
    )

    assert result.count == 3


def test_result_method_normalized():
    engine = StringSearchEngine(
        "banana"
    )

    result = engine.find(
        "ana",
        method="KMP",
    )

    assert result.method == "kmp"


def test_search_time_nonnegative():
    engine = StringSearchEngine(
        "banana"
    )

    result = engine.find(
        "ana"
    )

    assert result.search_time >= 0.0


def test_average_search_time_nonnegative():
    engine = StringSearchEngine(
        "banana"
    )

    engine.find(
        "ana"
    )

    result = engine.find(
        "na"
    )

    assert result.average_search_time >= 0.0


def test_suffix_array_preprocessing_recorded():
    engine = StringSearchEngine(
        "banana"
    )

    result = engine.find(
        "ana",
        method="sa",
    )

    assert result.preprocessing_time >= 0.0


def test_suffix_tree_preprocessing_recorded():
    engine = StringSearchEngine(
        "banana"
    )

    result = engine.find(
        "ana",
        method="tree",
    )

    assert result.preprocessing_time >= 0.0


def test_preprocess_suffix_array():
    engine = StringSearchEngine(
        "banana"
    )

    elapsed = engine.preprocess(
        "sa"
    )

    assert elapsed >= 0.0
    assert engine._suffix_array_index is not None


def test_preprocess_tree():
    engine = StringSearchEngine(
        "banana"
    )

    elapsed = engine.preprocess(
        "tree"
    )

    assert elapsed >= 0.0
    assert engine._suffix_tree is not None


def test_preprocess_kmp_is_zero():
    engine = StringSearchEngine(
        "banana"
    )

    assert engine.preprocess(
        "kmp"
    ) == 0.0


def test_empty_pattern_all_methods():
    engine = StringSearchEngine(
        "ABC"
    )

    results = engine.find_all(
        ""
    )

    for result in results.values():
        assert result.positions == [
            0,
            1,
            2,
            3,
        ]


def test_pattern_not_found_all_methods():
    engine = StringSearchEngine(
        "banana"
    )

    results = engine.find_all(
        "xyz"
    )

    for result in results.values():
        assert result.positions == []


def test_statistics_counts_queries():
    engine = StringSearchEngine(
        "banana"
    )

    engine.find(
        "ana",
        method="kmp",
    )

    engine.find(
        "na",
        method="kmp",
    )

    stats = engine.statistics()

    assert stats[
        "kmp"
    ][
        "queries"
    ] == 2


def test_statistics_unused_method_zero_queries():
    engine = StringSearchEngine(
        "banana"
    )

    stats = engine.statistics()

    assert stats[
        "rk"
    ][
        "queries"
    ] == 0


def test_recommend_single_query_kmp():
    engine = StringSearchEngine(
        "banana"
    )

    assert engine.recommend_method() == "kmp"


def test_recommend_repeated_queries_sa():
    engine = StringSearchEngine(
        "banana"
    )

    assert (
        engine.recommend_method(
            repeated_queries=True
        )
        == "sa"
    )


def test_recommend_multiple_patterns_rk():
    engine = StringSearchEngine(
        "banana"
    )

    assert (
        engine.recommend_method(
            multiple_patterns=True
        )
        == "rk"
    )


def test_recommend_prefix_queries_tree():
    engine = StringSearchEngine(
        "banana"
    )

    assert (
        engine.recommend_method(
            prefix_queries=True
        )
        == "tree"
    )


def test_nonstring_text_rejected():
    with pytest.raises(TypeError):
        StringSearchEngine(
            123
        )


def test_nonstring_pattern_rejected():
    engine = StringSearchEngine(
        "banana"
    )

    with pytest.raises(TypeError):
        engine.find(
            123
        )


def test_invalid_method_rejected():
    engine = StringSearchEngine(
        "banana"
    )

    with pytest.raises(ValueError):
        engine.find(
            "ana",
            method="unknown",
        )


def test_nonstring_method_rejected():
    engine = StringSearchEngine(
        "banana"
    )

    with pytest.raises(TypeError):
        engine.find(
            "ana",
            method=123,
        )


def test_invalid_recommendation_flag_rejected():
    engine = StringSearchEngine(
        "banana"
    )

    with pytest.raises(TypeError):
        engine.recommend_method(
            repeated_queries=1,
        )