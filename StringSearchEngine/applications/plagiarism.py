"""Plagiarism and document-similarity analysis."""

from dataclasses import dataclass
import re
from typing import List, Tuple

from StringSearchEngine.core.rabin_karp import (
    rabin_karp_search,
)
from StringSearchEngine.core.suffix_array import (
    build_lcp_array,
    build_suffix_array,
)


@dataclass
class PhraseMatch:
    """One overlapping phrase found in both documents."""

    phrase: str
    positions_a: List[int]
    positions_b: List[int]


@dataclass
class PlagiarismResult:
    """Summary of a document-similarity comparison."""

    similarity_score: float
    matched_phrases: List[PhraseMatch]
    longest_common_substring: str
    lcs_position_a: int
    lcs_position_b: int
    normalized_document_a: str
    normalized_document_b: str
    highlighted_a: str
    highlighted_b: str


def _normalize_document(
    document: str,
    case_sensitive: bool,
) -> str:
    """Normalize whitespace and optionally normalize case."""
    if not isinstance(
        document,
        str,
    ):
        raise TypeError(
            "document must be a string"
        )

    normalized = " ".join(
        document.split()
    )

    if not case_sensitive:
        normalized = normalized.lower()

    return normalized


def _word_shingles(
    text: str,
    phrase_words: int,
) -> List[
    Tuple[
        str,
        int,
    ]
]:
    """Return overlapping word phrases and their start positions."""
    matches = list(
        re.finditer(
            r"\S+",
            text,
        )
    )

    if len(
        matches
    ) < phrase_words:
        return []

    shingles = []

    for index in range(
        len(
            matches
        )
        - phrase_words
        + 1
    ):
        start = matches[
            index
        ].start()

        end = matches[
            index
            + phrase_words
            - 1
        ].end()

        shingles.append(
            (
                text[
                    start:end
                ],
                start,
            )
        )

    return shingles


def _choose_separator(
    first: str,
    second: str,
) -> str:
    """Choose one character not present in either document."""
    for code_point in range(
        1,
        256,
    ):
        candidate = chr(
            code_point
        )

        if (
            candidate not in first
            and candidate not in second
        ):
            return candidate

    code_point = 0xE000

    while True:
        candidate = chr(
            code_point
        )

        if (
            candidate not in first
            and candidate not in second
        ):
            return candidate

        code_point += 1


def longest_common_substring(
    document_a: str,
    document_b: str,
) -> Tuple[
    str,
    int,
    int,
]:
    """
    Find a longest common substring using a suffix array and LCP array.

    Returns:
        substring, position in document_a, position in document_b
    """
    if not isinstance(
        document_a,
        str,
    ):
        raise TypeError(
            "document_a must be a string"
        )

    if not isinstance(
        document_b,
        str,
    ):
        raise TypeError(
            "document_b must be a string"
        )

    if (
        not document_a
        or not document_b
    ):
        return (
            "",
            -1,
            -1,
        )

    separator = _choose_separator(
        document_a,
        document_b,
    )

    combined = (
        document_a
        + separator
        + document_b
    )

    boundary = len(
        document_a
    )

    second_start = boundary + 1

    suffix_array = build_suffix_array(
        combined
    )

    lcp = build_lcp_array(
        combined,
        suffix_array,
    )

    best_length = 0
    best_a = -1
    best_b = -1

    def origin(
        suffix_start: int,
    ) -> str:
        if suffix_start < boundary:
            return "a"

        if suffix_start > boundary:
            return "b"

        return "separator"

    for index, common_length in enumerate(
        lcp
    ):
        first_start = suffix_array[
            index
        ]

        second_suffix = suffix_array[
            index + 1
        ]

        first_origin = origin(
            first_start
        )

        second_origin = origin(
            second_suffix
        )

        if {
            first_origin,
            second_origin,
        } != {
            "a",
            "b",
        }:
            continue

        if common_length <= best_length:
            continue

        if first_origin == "a":
            position_a = first_start
            position_b = (
                second_suffix
                - second_start
            )
        else:
            position_a = second_suffix
            position_b = (
                first_start
                - second_start
            )

        best_length = common_length
        best_a = position_a
        best_b = position_b

    if best_length == 0:
        return (
            "",
            -1,
            -1,
        )

    return (
        document_a[
            best_a:
            best_a
            + best_length
        ],
        best_a,
        best_b,
    )


def _merge_intervals(
    intervals: List[
        Tuple[
            int,
            int,
        ]
    ],
) -> List[
    Tuple[
        int,
        int,
    ]
]:
    """Merge overlapping matched regions."""
    if not intervals:
        return []

    ordered = sorted(
        intervals
    )

    merged = [
        list(
            ordered[
                0
            ]
        )
    ]

    for start, end in ordered[
        1:
    ]:
        previous = merged[
            -1
        ]

        if start <= previous[
            1
        ]:
            previous[
                1
            ] = max(
                previous[
                    1
                ],
                end,
            )
        else:
            merged.append(
                [
                    start,
                    end,
                ]
            )

    return [
        (
            start,
            end,
        )
        for start, end in merged
    ]


def highlight_matched_regions(
    text: str,
    matches: List[PhraseMatch],
    document: str,
) -> str:
    """
    Highlight matched phrase regions using [[double brackets]].

    Positions refer to normalized documents.
    """
    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string"
        )

    if document not in {
        "a",
        "b",
    }:
        raise ValueError(
            "document must be 'a' or 'b'"
        )

    intervals = []

    for match in matches:
        positions = (
            match.positions_a
            if document == "a"
            else match.positions_b
        )

        for start in positions:
            intervals.append(
                (
                    start,
                    start
                    + len(
                        match.phrase
                    ),
                )
            )

    merged = _merge_intervals(
        intervals
    )

    if not merged:
        return text

    pieces = []

    cursor = 0

    for start, end in merged:
        pieces.append(
            text[
                cursor:start
            ]
        )

        pieces.append(
            "[["
        )

        pieces.append(
            text[
                start:end
            ]
        )

        pieces.append(
            "]]"
        )

        cursor = end

    pieces.append(
        text[
            cursor:
        ]
    )

    return "".join(
        pieces
    )


def analyze_plagiarism(
    document_a: str,
    document_b: str,
    phrase_words: int = 3,
    case_sensitive: bool = False,
) -> PlagiarismResult:
    """
    Compare two documents using overlapping word phrases.

    Rabin-Karp identifies shared phrases.
    A suffix array and LCP array identify a longest common substring.

    Similarity is the Jaccard score of unique word shingles:
        shared shingles / union of shingles
    """
    if (
        isinstance(
            phrase_words,
            bool,
        )
        or not isinstance(
            phrase_words,
            int,
        )
    ):
        raise TypeError(
            "phrase_words must be an integer"
        )

    if phrase_words <= 0:
        raise ValueError(
            "phrase_words must be positive"
        )

    if not isinstance(
        case_sensitive,
        bool,
    ):
        raise TypeError(
            "case_sensitive must be boolean"
        )

    normalized_a = _normalize_document(
        document_a,
        case_sensitive,
    )

    normalized_b = _normalize_document(
        document_b,
        case_sensitive,
    )

    shingles_a = _word_shingles(
        normalized_a,
        phrase_words,
    )

    shingles_b = _word_shingles(
        normalized_b,
        phrase_words,
    )

    phrases_a = {
        phrase
        for phrase, _ in shingles_a
    }

    phrases_b = {
        phrase
        for phrase, _ in shingles_b
    }

    positions_a = {}

    for phrase, start in shingles_a:
        positions_a.setdefault(
            phrase,
            [],
        ).append(
            start
        )

    matched_phrases = []

    for phrase in sorted(
        phrases_a
    ):
        positions_b = rabin_karp_search(
            normalized_b,
            phrase,
        )

        if positions_b:
            matched_phrases.append(
                PhraseMatch(
                    phrase=phrase,
                    positions_a=positions_a[
                        phrase
                    ],
                    positions_b=positions_b,
                )
            )

    union = (
        phrases_a
        | phrases_b
    )

    if union:
        similarity_score = (
            len(
                phrases_a
                & phrases_b
            )
            / len(
                union
            )
        )
    else:
        similarity_score = (
            1.0
            if normalized_a == normalized_b
            else 0.0
        )

    (
        common_substring,
        lcs_position_a,
        lcs_position_b,
    ) = longest_common_substring(
        normalized_a,
        normalized_b,
    )

    highlighted_a = highlight_matched_regions(
        normalized_a,
        matched_phrases,
        "a",
    )

    highlighted_b = highlight_matched_regions(
        normalized_b,
        matched_phrases,
        "b",
    )

    return PlagiarismResult(
        similarity_score=similarity_score,
        matched_phrases=matched_phrases,
        longest_common_substring=common_substring,
        lcs_position_a=lcs_position_a,
        lcs_position_b=lcs_position_b,
        normalized_document_a=normalized_a,
        normalized_document_b=normalized_b,
        highlighted_a=highlighted_a,
        highlighted_b=highlighted_b,
    )