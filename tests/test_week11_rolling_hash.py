"""Tests for Week 11 rolling-hash utilities."""

import pytest

from StringSearchEngine.utils.rolling_hash import (
    DEFAULT_BASE,
    DEFAULT_MODULUS,
    RollingHash,
    polynomial_hash,
)


def test_empty_string_hash_is_zero():
    assert polynomial_hash(
        ""
    ) == 0


def test_hash_is_deterministic():
    first = polynomial_hash(
        "algorithm"
    )

    second = polynomial_hash(
        "algorithm"
    )

    assert first == second


def test_different_strings_usually_differ():
    first = polynomial_hash(
        "algorithm"
    )

    second = polynomial_hash(
        "algorithms"
    )

    assert first != second


def test_custom_base_and_modulus():
    value = polynomial_hash(
        "abc",
        base=31,
        modulus=101,
    )

    expected = (
        (
            (
                ord(
                    "a"
                )
                * 31
                + ord(
                    "b"
                )
            )
            * 31
            + ord(
                "c"
            )
        )
        % 101
    )

    assert value == expected


def test_default_parameters_are_available():
    assert DEFAULT_BASE == 256
    assert DEFAULT_MODULUS == 1_000_000_007


def test_rolling_hash_initial_value():
    rolling = RollingHash(
        "abc"
    )

    assert rolling.value == polynomial_hash(
        "abc"
    )


def test_slide_matches_recomputed_hash():
    rolling = RollingHash(
        "abc"
    )

    value = rolling.slide(
        "a",
        "d",
    )

    assert rolling.window == "bcd"

    assert value == polynomial_hash(
        "bcd"
    )


def test_multiple_slides_match_recomputation():
    rolling = RollingHash(
        "abc"
    )

    rolling.slide(
        "a",
        "d",
    )

    rolling.slide(
        "b",
        "e",
    )

    rolling.slide(
        "c",
        "f",
    )

    assert rolling.window == "def"

    assert rolling.value == polynomial_hash(
        "def"
    )


def test_matches_same_window():
    rolling = RollingHash(
        "pattern"
    )

    assert rolling.matches(
        "pattern"
    ) is True


def test_matches_different_window():
    rolling = RollingHash(
        "pattern"
    )

    assert rolling.matches(
        "otherxx"
    ) is False


def test_matches_wrong_length():
    rolling = RollingHash(
        "abc"
    )

    assert rolling.matches(
        "abcd"
    ) is False


def test_small_modulus_supported():
    rolling = RollingHash(
        "abc",
        base=10,
        modulus=7,
    )

    assert rolling.value == polynomial_hash(
        "abc",
        base=10,
        modulus=7,
    )


def test_nonstring_hash_input_rejected():
    with pytest.raises(TypeError):
        polynomial_hash(
            123
        )


def test_empty_rolling_window_rejected():
    with pytest.raises(ValueError):
        RollingHash(
            ""
        )


def test_invalid_base_rejected():
    with pytest.raises(ValueError):
        polynomial_hash(
            "abc",
            base=0,
        )


def test_invalid_modulus_rejected():
    with pytest.raises(ValueError):
        polynomial_hash(
            "abc",
            modulus=1,
        )


def test_invalid_outgoing_character_rejected():
    rolling = RollingHash(
        "abc"
    )

    with pytest.raises(ValueError):
        rolling.slide(
            "x",
            "d",
        )


def test_multicharacter_incoming_rejected():
    rolling = RollingHash(
        "abc"
    )

    with pytest.raises(ValueError):
        rolling.slide(
            "a",
            "de",
        )