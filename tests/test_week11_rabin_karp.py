"""Tests for Week 11 Rabin-Karp string matching."""

import pytest

from StringSearchEngine.core.rabin_karp import (
    RabinKarpResult,
    rabin_karp_multi_search,
    rabin_karp_search,
    rabin_karp_search_with_stats,
)


def test_single_match():
    assert rabin_karp_search(
        "HELLO WORLD",
        "WORLD",
    ) == [
        6
    ]


def test_multiple_matches():
    assert rabin_karp_search(
        "ABCABCABC",
        "ABC",
    ) == [
        0,
        3,
        6,
    ]


def test_overlapping_matches():
    assert rabin_karp_search(
        "AAAAA",
        "AAA",
    ) == [
        0,
        1,
        2,
    ]


def test_pattern_equal_text():
    assert rabin_karp_search(
        "ALGORITHM",
        "ALGORITHM",
    ) == [
        0
    ]


def test_pattern_not_found():
    assert rabin_karp_search(
        "ADVANCED ALGORITHMS",
        "STRING",
    ) == []


def test_pattern_longer_than_text():
    assert rabin_karp_search(
        "ABC",
        "ABCDEFG",
    ) == []


def test_empty_text():
    assert rabin_karp_search(
        "",
        "A",
    ) == []


def test_empty_pattern_matches_boundaries():
    assert rabin_karp_search(
        "ABC",
        "",
    ) == [
        0,
        1,
        2,
        3,
    ]


def test_case_sensitive_search():
    assert rabin_karp_search(
        "String string STRING",
        "string",
    ) == [
        7
    ]


def test_unicode_search():
    assert rabin_karp_search(
        "αβγαβγ",
        "βγ",
    ) == [
        1,
        4,
    ]


def test_stats_result_type():
    result = rabin_karp_search_with_stats(
        "ABCABC",
        "ABC",
    )

    assert isinstance(
        result,
        RabinKarpResult,
    )


def test_stats_window_count():
    result = rabin_karp_search_with_stats(
        "ABCDEFG",
        "ABC",
    )

    assert result.windows_checked == 5


def test_stats_hash_hits_include_matches():
    result = rabin_karp_search_with_stats(
        "ABCABC",
        "ABC",
    )

    assert result.hash_hits >= 2


def test_default_good_hash_has_no_collision_here():
    result = rabin_karp_search_with_stats(
        "ABCABC",
        "ABC",
    )

    assert result.collisions == 0


def test_collision_can_be_demonstrated():
    result = rabin_karp_search_with_stats(
        "BA",
        "AB",
        base=1,
        modulus=2,
    )

    assert result.matches == []
    assert result.hash_hits == 1
    assert result.collisions == 1


def test_collision_does_not_create_false_match():
    result = rabin_karp_search_with_stats(
        "BA",
        "AB",
        base=1,
        modulus=2,
    )

    assert result.matches == []


def test_custom_base_and_modulus():
    assert rabin_karp_search(
        "XYZXYZ",
        "XYZ",
        base=31,
        modulus=101,
    ) == [
        0,
        3,
    ]


def test_multi_search_basic():
    result = rabin_karp_multi_search(
        "ABCABC",
        [
            "ABC",
            "BCA",
        ],
    )

    assert result[
        "ABC"
    ] == [
        0,
        3,
    ]

    assert result[
        "BCA"
    ] == [
        1
    ]


def test_multi_search_different_lengths():
    result = rabin_karp_multi_search(
        "BANANA",
        [
            "ANA",
            "BANANA",
            "NA",
        ],
    )

    assert result[
        "ANA"
    ] == [
        1,
        3,
    ]

    assert result[
        "BANANA"
    ] == [
        0
    ]

    assert result[
        "NA"
    ] == [
        2,
        4,
    ]


def test_multi_search_duplicate_patterns_removed():
    result = rabin_karp_multi_search(
        "AAAA",
        [
            "AA",
            "AA",
        ],
    )

    assert list(
        result.keys()
    ) == [
        "AA"
    ]

    assert result[
        "AA"
    ] == [
        0,
        1,
        2,
    ]


def test_multi_search_empty_pattern():
    result = rabin_karp_multi_search(
        "ABC",
        [
            "",
            "A",
        ],
    )

    assert result[
        ""
    ] == [
        0,
        1,
        2,
        3,
    ]


def test_multi_search_empty_pattern_list():
    assert rabin_karp_multi_search(
        "ABC",
        [],
    ) == {}


def test_multi_search_long_pattern():
    result = rabin_karp_multi_search(
        "ABC",
        [
            "ABCDEFG"
        ],
    )

    assert result[
        "ABCDEFG"
    ] == []


def test_nonstring_text_rejected():
    with pytest.raises(TypeError):
        rabin_karp_search(
            123,
            "ABC",
        )


def test_nonstring_pattern_rejected():
    with pytest.raises(TypeError):
        rabin_karp_search(
            "ABC",
            123,
        )


def test_invalid_patterns_container_rejected():
    with pytest.raises(TypeError):
        rabin_karp_multi_search(
            "ABC",
            {
                "A",
                "B",
            },
        )


def test_nonstring_pattern_in_batch_rejected():
    with pytest.raises(TypeError):
        rabin_karp_multi_search(
            "ABC",
            [
                "A",
                123,
            ],
        )