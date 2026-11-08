"""Tests for Week 11 plagiarism and document similarity."""

import pytest

from StringSearchEngine.applications.plagiarism import (
    PhraseMatch,
    PlagiarismResult,
    analyze_plagiarism,
    highlight_matched_regions,
    longest_common_substring,
)


def test_returns_result_object():
    result = analyze_plagiarism(
        "the quick brown fox",
        "the quick brown fox",
    )

    assert isinstance(
        result,
        PlagiarismResult,
    )


def test_identical_documents_score_one():
    result = analyze_plagiarism(
        "the quick brown fox",
        "the quick brown fox",
    )

    assert result.similarity_score == 1.0


def test_unrelated_documents_score_zero():
    result = analyze_plagiarism(
        "alpha beta gamma",
        "one two three",
    )

    assert result.similarity_score == 0.0


def test_partial_similarity():
    result = analyze_plagiarism(
        "the quick brown fox jumps",
        "slow quick brown fox sleeps",
        phrase_words=3,
    )

    assert result.similarity_score == pytest.approx(
        0.2
    )


def test_shared_phrase_detected():
    result = analyze_plagiarism(
        "the quick brown fox jumps",
        "slow quick brown fox sleeps",
        phrase_words=3,
    )

    phrases = [
        match.phrase
        for match in result.matched_phrases
    ]

    assert "quick brown fox" in phrases


def test_phrase_match_type():
    result = analyze_plagiarism(
        "one two three",
        "one two three",
        phrase_words=2,
    )

    assert isinstance(
        result.matched_phrases[
            0
        ],
        PhraseMatch,
    )


def test_phrase_positions_a():
    result = analyze_plagiarism(
        "one two one two",
        "one two",
        phrase_words=2,
    )

    match = next(
        item
        for item in result.matched_phrases
        if item.phrase == "one two"
    )

    assert match.positions_a == [
        0,
        8,
    ]


def test_phrase_positions_b():
    result = analyze_plagiarism(
        "one two",
        "zero one two one two",
        phrase_words=2,
    )

    match = next(
        item
        for item in result.matched_phrases
        if item.phrase == "one two"
    )

    assert match.positions_b == [
        5,
        13,
    ]


def test_highlight_document_a():
    result = analyze_plagiarism(
        "quick brown fox",
        "quick brown fox",
        phrase_words=3,
    )

    assert result.highlighted_a == (
        "[[quick brown fox]]"
    )


def test_highlight_document_b():
    result = analyze_plagiarism(
        "quick brown fox",
        "quick brown fox",
        phrase_words=3,
    )

    assert result.highlighted_b == (
        "[[quick brown fox]]"
    )


def test_overlapping_regions_merge():
    result = analyze_plagiarism(
        "one two three four",
        "one two three four",
        phrase_words=2,
    )

    assert result.highlighted_a == (
        "[[one two three four]]"
    )


def test_lcs_basic():
    substring, _, _ = (
        longest_common_substring(
            "banana",
            "ananas",
        )
    )

    assert substring == "anana"


def test_lcs_positions():
    substring, position_a, position_b = (
        longest_common_substring(
            "XXHELLOYY",
            "AAHELLOBB",
        )
    )

    assert substring == "HELLO"
    assert position_a == 2
    assert position_b == 2


def test_lcs_no_common_substring():
    result = longest_common_substring(
        "ABC",
        "xyz",
    )

    assert result == (
        "",
        -1,
        -1,
    )


def test_lcs_empty_document():
    result = longest_common_substring(
        "",
        "ABC",
    )

    assert result == (
        "",
        -1,
        -1,
    )


def test_lcs_unicode():
    substring, _, _ = (
        longest_common_substring(
            "αβγδε",
            "xxβγδyy",
        )
    )

    assert substring == "βγδ"


def test_empty_documents_score_one():
    result = analyze_plagiarism(
        "",
        "",
    )

    assert result.similarity_score == 1.0


def test_one_empty_document_score_zero():
    result = analyze_plagiarism(
        "",
        "some words here",
    )

    assert result.similarity_score == 0.0


def test_phrase_words_one():
    result = analyze_plagiarism(
        "red green blue",
        "green yellow",
        phrase_words=1,
    )

    assert result.similarity_score == pytest.approx(
        0.25
    )


def test_phrase_size_larger_than_documents():
    result = analyze_plagiarism(
        "one two",
        "one two",
        phrase_words=5,
    )

    assert result.similarity_score == 1.0
    assert result.matched_phrases == []


def test_default_is_case_insensitive():
    result = analyze_plagiarism(
        "The Quick Brown Fox",
        "the quick brown fox",
    )

    assert result.similarity_score == 1.0


def test_case_sensitive_mode():
    result = analyze_plagiarism(
        "The Quick Brown Fox",
        "the quick brown fox",
        case_sensitive=True,
    )

    assert result.similarity_score == 0.0


def test_whitespace_normalization():
    result = analyze_plagiarism(
        "one   two\nthree",
        "one two three",
    )

    assert (
        result.normalized_document_a
        == "one two three"
    )

    assert (
        result.normalized_document_b
        == "one two three"
    )


def test_direct_highlight_helper():
    matches = [
        PhraseMatch(
            phrase="two three",
            positions_a=[
                4
            ],
            positions_b=[
                0
            ],
        )
    ]

    highlighted = highlight_matched_regions(
        "one two three four",
        matches,
        "a",
    )

    assert highlighted == (
        "one [[two three]] four"
    )


def test_highlight_no_matches():
    assert highlight_matched_regions(
        "plain text",
        [],
        "a",
    ) == "plain text"


def test_invalid_document_a_rejected():
    with pytest.raises(TypeError):
        analyze_plagiarism(
            123,
            "text",
        )


def test_invalid_document_b_rejected():
    with pytest.raises(TypeError):
        analyze_plagiarism(
            "text",
            123,
        )


def test_invalid_phrase_words_type_rejected():
    with pytest.raises(TypeError):
        analyze_plagiarism(
            "text",
            "text",
            phrase_words=True,
        )


def test_nonpositive_phrase_words_rejected():
    with pytest.raises(ValueError):
        analyze_plagiarism(
            "text",
            "text",
            phrase_words=0,
        )


def test_invalid_case_sensitive_rejected():
    with pytest.raises(TypeError):
        analyze_plagiarism(
            "text",
            "text",
            case_sensitive="no",
        )


def test_invalid_highlight_document_rejected():
    with pytest.raises(ValueError):
        highlight_matched_regions(
            "text",
            [],
            "c",
        )


def test_lcs_invalid_first_document_rejected():
    with pytest.raises(TypeError):
        longest_common_substring(
            123,
            "ABC",
        )


def test_lcs_invalid_second_document_rejected():
    with pytest.raises(TypeError):
        longest_common_substring(
            "ABC",
            123,
        )