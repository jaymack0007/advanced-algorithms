"""Tests for Week 11 Knuth-Morris-Pratt string matching."""

import pytest

from StringSearchEngine.core.kmp import (
    KMPTraceResult,
    compute_lps,
    kmp_search,
    kmp_search_with_trace,
)


def test_lps_empty_pattern():
    assert compute_lps(
        ""
    ) == []


def test_lps_single_character():
    assert compute_lps(
        "A"
    ) == [
        0
    ]


def test_lps_no_repeated_prefix():
    assert compute_lps(
        "ABCD"
    ) == [
        0,
        0,
        0,
        0,
    ]


def test_lps_repeated_characters():
    assert compute_lps(
        "AAAA"
    ) == [
        0,
        1,
        2,
        3,
    ]


def test_lps_periodic_pattern():
    assert compute_lps(
        "ABABAC"
    ) == [
        0,
        0,
        1,
        2,
        3,
        0,
    ]


def test_lps_classic_pattern():
    assert compute_lps(
        "ABABCABAB"
    ) == [
        0,
        0,
        1,
        2,
        0,
        1,
        2,
        3,
        4,
    ]


def test_single_match():
    assert kmp_search(
        "HELLO WORLD",
        "WORLD",
    ) == [
        6
    ]


def test_multiple_matches():
    assert kmp_search(
        "ABCABCABC",
        "ABC",
    ) == [
        0,
        3,
        6,
    ]


def test_overlapping_matches():
    assert kmp_search(
        "AAAAA",
        "AAA",
    ) == [
        0,
        1,
        2,
    ]


def test_pattern_longer_than_text():
    assert kmp_search(
        "ABC",
        "ABCDEFG",
    ) == []


def test_pattern_equal_to_text():
    assert kmp_search(
        "ALGORITHM",
        "ALGORITHM",
    ) == [
        0
    ]


def test_pattern_not_found():
    assert kmp_search(
        "ADVANCED ALGORITHMS",
        "STRING",
    ) == []


def test_empty_text_nonempty_pattern():
    assert kmp_search(
        "",
        "ABC",
    ) == []


def test_empty_pattern_matches_boundaries():
    assert kmp_search(
        "ABC",
        "",
    ) == [
        0,
        1,
        2,
        3,
    ]


def test_periodic_text():
    assert kmp_search(
        "ABABABAB",
        "ABAB",
    ) == [
        0,
        2,
        4,
    ]


def test_case_sensitive_search():
    assert kmp_search(
        "String string STRING",
        "string",
    ) == [
        7
    ]


def test_unicode_search():
    assert kmp_search(
        "αβγαβγ",
        "βγ",
    ) == [
        1,
        4,
    ]


def test_trace_returns_result_object():
    result = kmp_search_with_trace(
        "ABCABC",
        "ABC",
    )

    assert isinstance(
        result,
        KMPTraceResult,
    )


def test_trace_contains_lps():
    result = kmp_search_with_trace(
        "ABABAB",
        "ABAB",
    )

    assert result.lps == [
        0,
        0,
        1,
        2,
    ]


def test_trace_counts_fallbacks():
    result = kmp_search_with_trace(
        "ABABABC",
        "ABABC",
    )

    assert result.fallbacks > 0


def test_trace_counts_comparisons():
    result = kmp_search_with_trace(
        "ABCABCABC",
        "ABC",
    )

    assert result.comparisons > 0


def test_nonstring_text_rejected():
    with pytest.raises(TypeError):
        kmp_search(
            123,
            "ABC",
        )


def test_nonstring_pattern_rejected():
    with pytest.raises(TypeError):
        kmp_search(
            "ABC",
            123,
        )


def test_nonstring_lps_pattern_rejected():
    with pytest.raises(TypeError):
        compute_lps(
            [
                "A",
                "B",
            ]
        )