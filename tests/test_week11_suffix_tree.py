"""Tests for the Week 11 compressed suffix tree."""

import pytest

from StringSearchEngine.core.suffix_tree import (
    CompressedSuffixTree,
    SuffixTree,
)


def test_empty_tree():
    tree = CompressedSuffixTree(
        ""
    )

    assert tree.find(
        "A"
    ) == []


def test_empty_tree_empty_pattern():
    tree = CompressedSuffixTree(
        ""
    )

    assert tree.find(
        ""
    ) == [
        0
    ]


def test_single_character():
    tree = CompressedSuffixTree(
        "A"
    )

    assert tree.find(
        "A"
    ) == [
        0
    ]


def test_banana_search():
    tree = CompressedSuffixTree(
        "banana"
    )

    assert tree.find(
        "ana"
    ) == [
        1,
        3,
    ]


def test_overlapping_matches():
    tree = CompressedSuffixTree(
        "AAAAA"
    )

    assert tree.find(
        "AAA"
    ) == [
        0,
        1,
        2,
    ]


def test_pattern_equal_text():
    tree = CompressedSuffixTree(
        "ALGORITHM"
    )

    assert tree.find(
        "ALGORITHM"
    ) == [
        0
    ]


def test_pattern_not_found():
    tree = CompressedSuffixTree(
        "ADVANCED ALGORITHMS"
    )

    assert tree.find(
        "STRING"
    ) == []


def test_pattern_longer_than_text():
    tree = CompressedSuffixTree(
        "ABC"
    )

    assert tree.find(
        "ABCDEFG"
    ) == []


def test_empty_pattern_matches_boundaries():
    tree = CompressedSuffixTree(
        "ABC"
    )

    assert tree.find(
        ""
    ) == [
        0,
        1,
        2,
        3,
    ]


def test_case_sensitive():
    tree = CompressedSuffixTree(
        "String string STRING"
    )

    assert tree.find(
        "string"
    ) == [
        7
    ]


def test_unicode_search():
    tree = CompressedSuffixTree(
        "αβγαβγ"
    )

    assert tree.find(
        "βγ"
    ) == [
        1,
        4,
    ]


def test_single_character_suffix_occurrences():
    tree = CompressedSuffixTree(
        "banana"
    )

    assert tree.find(
        "a"
    ) == [
        1,
        3,
        5,
    ]


def test_contains_true():
    tree = CompressedSuffixTree(
        "banana"
    )

    assert tree.contains(
        "nan"
    ) is True


def test_contains_false():
    tree = CompressedSuffixTree(
        "banana"
    )

    assert tree.contains(
        "apple"
    ) is False


def test_contains_empty_pattern():
    tree = CompressedSuffixTree(
        "banana"
    )

    assert tree.contains(
        ""
    ) is True


def test_prefix_matches():
    tree = CompressedSuffixTree(
        "banana"
    )

    assert tree.prefix_matches(
        "ba"
    ) == [
        0
    ]


def test_prefix_matches_multiple_suffixes():
    tree = CompressedSuffixTree(
        "banana"
    )

    assert tree.prefix_matches(
        "an"
    ) == [
        1,
        3,
    ]


def test_longest_repeated_substring_banana():
    tree = CompressedSuffixTree(
        "banana"
    )

    assert (
        tree.longest_repeated_substring()
        == "ana"
    )


def test_longest_repeated_substring_repeated_chars():
    tree = CompressedSuffixTree(
        "aaaa"
    )

    assert (
        tree.longest_repeated_substring()
        == "aaa"
    )


def test_no_repeated_substring():
    tree = CompressedSuffixTree(
        "abcd"
    )

    assert (
        tree.longest_repeated_substring()
        == ""
    )


def test_distinct_substrings_empty():
    tree = CompressedSuffixTree(
        ""
    )

    assert (
        tree.distinct_substring_count()
        == 0
    )


def test_distinct_substrings_single_character():
    tree = CompressedSuffixTree(
        "A"
    )

    assert (
        tree.distinct_substring_count()
        == 1
    )


def test_distinct_substrings_banana():
    tree = CompressedSuffixTree(
        "banana"
    )

    assert (
        tree.distinct_substring_count()
        == 15
    )


def test_distinct_substrings_repeated_chars():
    tree = CompressedSuffixTree(
        "aaaa"
    )

    assert (
        tree.distinct_substring_count()
        == 4
    )


def test_tree_is_compressed():
    tree = CompressedSuffixTree(
        "banana"
    )

    assert (
        tree.root.edges[
            "b"
        ].label
        == "banana"
    )


def test_statistics_suffix_count():
    tree = CompressedSuffixTree(
        "banana"
    )

    stats = tree.statistics()

    assert stats[
        "suffixes"
    ] == 6

    assert stats[
        "nodes"
    ] > 0

    assert stats[
        "edges"
    ] > 0


def test_edge_records_available():
    tree = CompressedSuffixTree(
        "banana"
    )

    records = tree.edge_records()

    assert records

    assert all(
        len(
            record
        ) == 3
        for record in records
    )


def test_suffix_tree_alias():
    tree = SuffixTree(
        "banana"
    )

    assert isinstance(
        tree,
        CompressedSuffixTree,
    )


def test_nonstring_text_rejected():
    with pytest.raises(TypeError):
        CompressedSuffixTree(
            123
        )


def test_nonstring_pattern_rejected():
    tree = CompressedSuffixTree(
        "ABC"
    )

    with pytest.raises(TypeError):
        tree.find(
            123
        )


def test_nonstring_prefix_rejected():
    tree = CompressedSuffixTree(
        "ABC"
    )

    with pytest.raises(TypeError):
        tree.prefix_matches(
            123
        )