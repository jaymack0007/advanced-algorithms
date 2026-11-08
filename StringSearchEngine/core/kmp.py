"""Knuth-Morris-Pratt string matching."""

from dataclasses import dataclass
from typing import List


@dataclass
class KMPTraceResult:
    """Detailed KMP search result for analysis and visualization."""

    matches: List[int]
    lps: List[int]
    comparisons: int
    fallbacks: int


def compute_lps(
    pattern: str,
) -> List[int]:
    """
    Compute the longest proper prefix that is also a suffix table.

    For each pattern position i, lps[i] stores the length of the
    longest proper prefix of pattern[0:i+1] that is also a suffix.

    Complexity:
        O(m) time
        O(m) space
    """
    if not isinstance(
        pattern,
        str,
    ):
        raise TypeError(
            "pattern must be a string"
        )

    if not pattern:
        return []

    lps = [
        0
    ] * len(
        pattern
    )

    prefix_length = 0
    index = 1

    while index < len(
        pattern
    ):
        if (
            pattern[
                index
            ]
            == pattern[
                prefix_length
            ]
        ):
            prefix_length += 1

            lps[
                index
            ] = prefix_length

            index += 1

        elif prefix_length > 0:
            prefix_length = lps[
                prefix_length - 1
            ]

        else:
            lps[
                index
            ] = 0

            index += 1

    return lps


def kmp_search_with_trace(
    text: str,
    pattern: str,
) -> KMPTraceResult:
    """
    Search for every occurrence of pattern in text using KMP.

    Overlapping matches are included.

    Empty-pattern behavior:
        The empty pattern matches at every valid boundary,
        positions 0 through len(text).

    Complexity:
        O(n + m) time
        O(m) additional space
    """
    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string"
        )

    if not isinstance(
        pattern,
        str,
    ):
        raise TypeError(
            "pattern must be a string"
        )

    if pattern == "":
        return KMPTraceResult(
            matches=list(
                range(
                    len(
                        text
                    )
                    + 1
                )
            ),
            lps=[],
            comparisons=0,
            fallbacks=0,
        )

    if len(
        pattern
    ) > len(
        text
    ):
        return KMPTraceResult(
            matches=[],
            lps=compute_lps(
                pattern
            ),
            comparisons=0,
            fallbacks=0,
        )

    lps = compute_lps(
        pattern
    )

    matches = []

    text_index = 0
    pattern_index = 0

    comparisons = 0
    fallbacks = 0

    while text_index < len(
        text
    ):
        comparisons += 1

        if (
            text[
                text_index
            ]
            == pattern[
                pattern_index
            ]
        ):
            text_index += 1
            pattern_index += 1

            if pattern_index == len(
                pattern
            ):
                matches.append(
                    text_index
                    - pattern_index
                )

                pattern_index = lps[
                    pattern_index - 1
                ]

        elif pattern_index > 0:
            pattern_index = lps[
                pattern_index - 1
            ]

            fallbacks += 1

        else:
            text_index += 1

    return KMPTraceResult(
        matches=matches,
        lps=lps,
        comparisons=comparisons,
        fallbacks=fallbacks,
    )


def kmp_search(
    text: str,
    pattern: str,
) -> List[int]:
    """
    Return all starting positions of pattern in text using KMP.

    This is the simple public search function. For instrumentation,
    use kmp_search_with_trace().
    """
    return kmp_search_with_trace(
        text,
        pattern,
    ).matches