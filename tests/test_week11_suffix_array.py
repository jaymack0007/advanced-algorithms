"""Tests for Week 11 suffix arrays and LCP construction."""

import pytest

from StringSearchEngine.core.suffix_array import (
    SuffixArrayIndex,
    build_lcp_array,
    build_suffix_array,
    suffix_array_search,
)


def test_empty_suffix_array():
    assert build_suffix_array(
        ""
    ) == []


def test_single_character_suffix_array():
    assert build_suffix_array(
        "A"
    ) == [
        0
    ]


def test_banana_suffix_array():
    assert build_suffix_array(
        "banana"
    ) == [
        5,
        3,
        1,
        0,
        4,
        2,
    ]


def test_repeated_character_suffix_array():
    assert build_suffix_array(
        "aaaa"
    ) == [
        3,
        2,
        1,
        0,
    ]


def test_suffix_array_is_permutation():
    text = "mississippi"

    suffix_array = build_suffix_array(
        text
    )

    assert sorted(
        suffix_array
    ) == list(
        range(
            len(
                text
            )
        )
    )


def test_suffixes_are_lexicographically_sorted():
    text = "advanced"

    suffix_array = build_suffix_array(
        text
    )

    suffixes = [
        text[
            index:
        ]
        for index in suffix_array
    ]

    assert suffixes == sorted(
        suffixes
    )


def test_unicode_suffix_array():
    text = "βαβα"

    suffix_array = build_suffix_array(
        text
    )

    suffixes = [
        text[
            index:
        ]
        for index in suffix_array
    ]

    assert suffixes == sorted(
        suffixes
    )


def test_empty_lcp():
    assert build_lcp_array(
        ""
    ) == []


def test_single_character_lcp():
    assert build_lcp_array(
        "A"
    ) == []


def test_banana_lcp():
    text = "banana"

    suffix_array = [
        5,
        3,
        1,
        0,
        4,
        2,
    ]

    assert build_lcp_array(
        text,
        suffix_array,
    ) == [
        1,
        3,
        0,
        0,
        2,
    ]


def test_repeated_character_lcp():
    assert build_lcp_array(
        "aaaa"
    ) == [
        1,
        2,
        3,
    ]


def test_search_single_match():
    assert suffix_array_search(
        "HELLO WORLD",
        "WORLD",
    ) == [
        6
    ]


def test_search_multiple_matches():
    assert suffix_array_search(
        "banana",
        "ana",
    ) == [
        1,
        3,
    ]


def test_search_overlapping_matches():
    assert suffix_array_search(
        "AAAAA",
        "AAA",
    ) == [
        0,
        1,
        2,
    ]


def test_search_pattern_equal_text():
    assert suffix_array_search(
        "ALGORITHM",
        "ALGORITHM",
    ) == [
        0
    ]


def test_search_pattern_not_found():
    assert suffix_array_search(
        "ADVANCED ALGORITHMS",
        "STRING",
    ) == []


def test_search_pattern_longer_than_text():
    assert suffix_array_search(
        "ABC",
        "ABCDEFG",
    ) == []


def test_search_empty_pattern():
    assert suffix_array_search(
        "ABC",
        "",
    ) == [
        0,
        1,
        2,
        3,
    ]


def test_search_with_prebuilt_suffix_array():
    text = "BANANA"

    suffix_array = build_suffix_array(
        text
    )

    assert suffix_array_search(
        text,
        "ANA",
        suffix_array,
    ) == [
        1,
        3,
    ]


def test_search_case_sensitive():
    assert suffix_array_search(
        "String string STRING",
        "string",
    ) == [
        7
    ]


def test_index_builds_arrays():
    index = SuffixArrayIndex(
        "banana"
    )

    assert index.suffix_array == [
        5,
        3,
        1,
        0,
        4,
        2,
    ]

    assert index.lcp == [
        1,
        3,
        0,
        0,
        2,
    ]


def test_index_find():
    index = SuffixArrayIndex(
        "banana"
    )

    assert index.find(
        "na"
    ) == [
        2,
        4,
    ]


def test_longest_repeated_substring():
    index = SuffixArrayIndex(
        "banana"
    )

    assert index.longest_repeated_substring() == "ana"


def test_no_repeated_substring():
    index = SuffixArrayIndex(
        "abcd"
    )

    assert index.longest_repeated_substring() == ""


def test_distinct_substring_count():
    index = SuffixArrayIndex(
        "banana"
    )

    assert index.distinct_substring_count() == 15


def test_nonstring_text_rejected():
    with pytest.raises(TypeError):
        build_suffix_array(
            123
        )


def test_nonstring_pattern_rejected():
    with pytest.raises(TypeError):
        suffix_array_search(
            "ABC",
            123,
        )


def test_invalid_suffix_array_length_rejected():
    with pytest.raises(ValueError):
        build_lcp_array(
            "ABC",
            [
                0,
                1,
            ],
        )


def test_invalid_suffix_array_values_rejected():
    with pytest.raises(ValueError):
        suffix_array_search(
            "ABC",
            "A",
            [
                0,
                1,
                1,
            ],
        )