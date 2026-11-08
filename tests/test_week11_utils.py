"""Tests for Week 11 text-loading and generator utilities."""

import pytest

from StringSearchEngine.utils.generators import (
    DNA_ALPHABET,
    embed_pattern,
    random_dna,
    random_text,
    repetitive_text,
    sample_patterns,
)
from StringSearchEngine.utils.text_loader import (
    file_size_bytes,
    load_documents,
    load_lines,
    load_text,
    normalize_text,
)


def test_normalize_text_unchanged():
    assert normalize_text(
        "Hello World"
    ) == "Hello World"


def test_normalize_text_lowercase():
    assert normalize_text(
        "Hello World",
        lowercase=True,
    ) == "hello world"


def test_normalize_text_whitespace():
    assert normalize_text(
        "one   two\nthree",
        collapse_whitespace=True,
    ) == "one two three"


def test_normalize_text_both_options():
    assert normalize_text(
        "ONE   TWO",
        lowercase=True,
        collapse_whitespace=True,
    ) == "one two"


def test_normalize_nonstring_rejected():
    with pytest.raises(TypeError):
        normalize_text(
            123
        )


def test_load_text(tmp_path):
    path = (
        tmp_path
        / "sample.txt"
    )

    path.write_text(
        "Hello World",
        encoding="utf-8",
    )

    assert load_text(
        path
    ) == "Hello World"


def test_load_text_lowercase(tmp_path):
    path = (
        tmp_path
        / "sample.txt"
    )

    path.write_text(
        "HELLO",
        encoding="utf-8",
    )

    assert load_text(
        path,
        lowercase=True,
    ) == "hello"


def test_load_text_collapse_whitespace(tmp_path):
    path = (
        tmp_path
        / "sample.txt"
    )

    path.write_text(
        "one   two\nthree",
        encoding="utf-8",
    )

    assert load_text(
        path,
        collapse_whitespace=True,
    ) == "one two three"


def test_load_lines(tmp_path):
    path = (
        tmp_path
        / "sample.txt"
    )

    path.write_text(
        "one\ntwo\nthree",
        encoding="utf-8",
    )

    assert load_lines(
        path
    ) == [
        "one",
        "two",
        "three",
    ]


def test_load_lines_skip_empty(tmp_path):
    path = (
        tmp_path
        / "sample.txt"
    )

    path.write_text(
        "one\n\n two \n",
        encoding="utf-8",
    )

    assert load_lines(
        path,
        skip_empty=True,
    ) == [
        "one",
        " two ",
    ]


def test_load_documents(tmp_path):
    first = (
        tmp_path
        / "a.txt"
    )

    second = (
        tmp_path
        / "b.txt"
    )

    first.write_text(
        "alpha",
        encoding="utf-8",
    )

    second.write_text(
        "beta",
        encoding="utf-8",
    )

    documents = load_documents(
        [
            first,
            second,
        ]
    )

    assert documents[
        str(
            first
        )
    ] == "alpha"

    assert documents[
        str(
            second
        )
    ] == "beta"


def test_file_size_bytes(tmp_path):
    path = (
        tmp_path
        / "sample.txt"
    )

    path.write_bytes(
        b"ABCDE"
    )

    assert file_size_bytes(
        path
    ) == 5


def test_missing_file_rejected(tmp_path):
    with pytest.raises(
        FileNotFoundError
    ):
        load_text(
            tmp_path
            / "missing.txt"
        )


def test_directory_rejected(tmp_path):
    with pytest.raises(ValueError):
        load_text(
            tmp_path
        )


def test_load_documents_requires_list_or_tuple():
    with pytest.raises(TypeError):
        load_documents(
            {
                "a.txt"
            }
        )


def test_invalid_encoding_type_rejected(tmp_path):
    path = (
        tmp_path
        / "sample.txt"
    )

    path.write_text(
        "hello",
        encoding="utf-8",
    )

    with pytest.raises(TypeError):
        load_text(
            path,
            encoding=123,
        )


def test_random_text_length():
    assert len(
        random_text(
            100,
            seed=1,
        )
    ) == 100


def test_random_text_deterministic_seed():
    assert (
        random_text(
            50,
            seed=42,
        )
        == random_text(
            50,
            seed=42,
        )
    )


def test_random_text_uses_alphabet():
    result = random_text(
        100,
        alphabet="AB",
        seed=1,
    )

    assert set(
        result
    ) <= {
        "A",
        "B",
    }


def test_random_text_zero_length():
    assert random_text(
        0
    ) == ""


def test_random_text_negative_length_rejected():
    with pytest.raises(ValueError):
        random_text(
            -1
        )


def test_random_text_empty_alphabet_rejected():
    with pytest.raises(ValueError):
        random_text(
            10,
            alphabet="",
        )


def test_repetitive_text_basic():
    assert repetitive_text(
        8,
        pattern="ABC",
    ) == "ABCABCAB"


def test_repetitive_text_exact_length():
    assert len(
        repetitive_text(
            17,
            pattern="AB",
        )
    ) == 17


def test_repetitive_text_empty_pattern_rejected():
    with pytest.raises(ValueError):
        repetitive_text(
            10,
            pattern="",
        )


def test_random_dna_uses_valid_alphabet():
    result = random_dna(
        100,
        seed=10,
    )

    assert set(
        result
    ) <= set(
        DNA_ALPHABET
    )


def test_random_dna_can_include_n():
    result = random_dna(
        500,
        seed=10,
        include_n=True,
    )

    assert set(
        result
    ) <= set(
        "ACGTN"
    )


def test_random_dna_deterministic():
    assert (
        random_dna(
            50,
            seed=7,
        )
        == random_dna(
            50,
            seed=7,
        )
    )


def test_embed_pattern_once():
    assert embed_pattern(
        "abcdefghij",
        "XYZ",
        [
            2
        ],
    ) == "abXYZfghij"


def test_embed_pattern_multiple():
    assert embed_pattern(
        "abcdefghij",
        "XX",
        [
            0,
            8,
        ],
    ) == "XXcdefghXX"


def test_embed_pattern_out_of_bounds_rejected():
    with pytest.raises(ValueError):
        embed_pattern(
            "abc",
            "XYZ",
            [
                1
            ],
        )


def test_embed_pattern_nonstring_rejected():
    with pytest.raises(TypeError):
        embed_pattern(
            "abc",
            123,
            [
                0
            ],
        )


def test_sample_patterns_count():
    patterns = sample_patterns(
        "abcdefghij",
        pattern_length=3,
        count=4,
        seed=5,
    )

    assert len(
        patterns
    ) == 4


def test_sample_patterns_have_correct_length():
    patterns = sample_patterns(
        "abcdefghij",
        pattern_length=4,
        count=3,
        seed=2,
    )

    assert all(
        len(
            pattern
        ) == 4
        for pattern in patterns
    )


def test_sample_patterns_deterministic():
    assert (
        sample_patterns(
            "abcdefghij",
            3,
            4,
            seed=8,
        )
        == sample_patterns(
            "abcdefghij",
            3,
            4,
            seed=8,
        )
    )


def test_sample_pattern_length_too_large_rejected():
    with pytest.raises(ValueError):
        sample_patterns(
            "abc",
            pattern_length=4,
            count=1,
        )