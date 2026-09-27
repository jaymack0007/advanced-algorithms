"""Tests for Longest Common Subsequence implementations."""

from src.dp.lcs import (
    lcs_memoized,
    lcs_recursive,
    lcs_tabulated,
    reconstruct_lcs,
)


def test_lcs_recursive():
    assert lcs_recursive(
        "ABCBDAB",
        "BDCABA",
    ) == 4


def test_lcs_memoized():
    assert lcs_memoized(
        "ABCBDAB",
        "BDCABA",
    ) == 4


def test_lcs_tabulated():
    assert lcs_tabulated(
        "ABCBDAB",
        "BDCABA",
    ) == 4


def test_all_versions_match():
    x = "AGGTAB"
    y = "GXTXAYB"

    recursive = lcs_recursive(x, y)
    memoized = lcs_memoized(x, y)
    tabulated = lcs_tabulated(x, y)

    assert recursive == 4
    assert recursive == memoized
    assert memoized == tabulated


def test_reconstruct_lcs():
    sequence = reconstruct_lcs(
        "AGGTAB",
        "GXTXAYB",
    )

    assert sequence == "GTAB"


def test_empty_string():
    assert lcs_recursive("", "ABC") == 0
    assert lcs_memoized("", "ABC") == 0
    assert lcs_tabulated("", "ABC") == 0


def test_identical_strings():
    text = "DYNAMIC"

    assert lcs_recursive(text, text) == len(text)
    assert lcs_memoized(text, text) == len(text)
    assert lcs_tabulated(text, text) == len(text)


def test_no_common_subsequence():
    assert lcs_recursive(
        "ABC",
        "XYZ",
    ) == 0

    assert lcs_memoized(
        "ABC",
        "XYZ",
    ) == 0

    assert lcs_tabulated(
        "ABC",
        "XYZ",
    ) == 0


def test_recursive_stats():
    stats = {}

    result = lcs_recursive(
        "ABC",
        "AC",
        stats=stats,
    )

    assert result == 2
    assert stats["calls"] > 1
    assert stats["max_depth"] > 1


def test_memoized_uses_fewer_calls():
    x = "ABCDEFG"
    y = "ACEGXYZ"

    recursive_stats = {}
    memoized_stats = {}

    lcs_recursive(
        x,
        y,
        stats=recursive_stats,
    )

    lcs_memoized(
        x,
        y,
        stats=memoized_stats,
    )

    assert (
        memoized_stats["calls"]
        < recursive_stats["calls"]
    )


def test_large_tabulated_input():
    x = "A" * 100
    y = "A" * 100

    assert lcs_tabulated(x, y) == 100


def test_large_memoized_input():
    x = "A" * 100
    y = "A" * 100

    assert lcs_memoized(x, y) == 100