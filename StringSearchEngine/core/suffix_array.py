"""Suffix-array construction, LCP computation, and substring search."""

from dataclasses import dataclass
from typing import List, Optional


def _validate_text(
    text: str,
) -> None:
    """Require string input."""
    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string"
        )


def _validate_suffix_array(
    text: str,
    suffix_array: List[int],
) -> None:
    """Validate that a suffix array is a permutation of text indices."""
    if not isinstance(
        suffix_array,
        list,
    ):
        raise TypeError(
            "suffix_array must be a list"
        )

    if len(
        suffix_array
    ) != len(
        text
    ):
        raise ValueError(
            "suffix_array length must equal text length"
        )

    if sorted(
        suffix_array
    ) != list(
        range(
            len(
                text
            )
        )
    ):
        raise ValueError(
            "suffix_array must contain each text index exactly once"
        )


def _counting_sort(
    indices: List[int],
    keys: List[int],
    maximum_key: int,
) -> List[int]:
    """Stable counting sort used by prefix doubling."""
    counts = [
        0
    ] * (
        maximum_key
        + 1
    )

    for index in indices:
        counts[
            keys[
                index
            ]
        ] += 1

    positions = [
        0
    ] * len(
        counts
    )

    running = 0

    for key in range(
        len(
            counts
        )
    ):
        positions[
            key
        ] = running

        running += counts[
            key
        ]

    result = [
        0
    ] * len(
        indices
    )

    for index in indices:
        key = keys[
            index
        ]

        result[
            positions[
                key
            ]
        ] = index

        positions[
            key
        ] += 1

    return result


def build_suffix_array(
    text: str,
) -> List[int]:
    """
    Construct a suffix array using prefix doubling.

    Integer rank pairs are radix-sorted with counting sort.

    Complexity:
        O(n log n) time
        O(n) auxiliary space
    """
    _validate_text(
        text
    )

    length = len(
        text
    )

    if length == 0:
        return []

    if length == 1:
        return [
            0
        ]

    alphabet = {
        character: rank
        for rank, character in enumerate(
            sorted(
                set(
                    text
                )
            )
        )
    }

    ranks = [
        alphabet[
            character
        ]
        for character in text
    ]

    suffix_array = list(
        range(
            length
        )
    )

    offset = 1

    while offset < length:
        class_count = (
            max(
                ranks
            )
            + 1
        )

        first_keys = [
            ranks[
                index
            ]
            + 1
            for index in range(
                length
            )
        ]

        second_keys = [
            (
                ranks[
                    index
                    + offset
                ]
                + 1
            )
            if (
                index
                + offset
                < length
            )
            else 0
            for index in range(
                length
            )
        ]

        suffix_array = _counting_sort(
            suffix_array,
            second_keys,
            class_count,
        )

        suffix_array = _counting_sort(
            suffix_array,
            first_keys,
            class_count,
        )

        new_ranks = [
            0
        ] * length

        new_rank = 0

        new_ranks[
            suffix_array[
                0
            ]
        ] = 0

        for position in range(
            1,
            length,
        ):
            current = suffix_array[
                position
            ]

            previous = suffix_array[
                position - 1
            ]

            current_pair = (
                ranks[
                    current
                ],
                (
                    ranks[
                        current
                        + offset
                    ]
                    if (
                        current
                        + offset
                        < length
                    )
                    else -1
                ),
            )

            previous_pair = (
                ranks[
                    previous
                ],
                (
                    ranks[
                        previous
                        + offset
                    ]
                    if (
                        previous
                        + offset
                        < length
                    )
                    else -1
                ),
            )

            if current_pair != previous_pair:
                new_rank += 1

            new_ranks[
                current
            ] = new_rank

        ranks = new_ranks

        if new_rank == length - 1:
            break

        offset *= 2

    return suffix_array


def build_lcp_array(
    text: str,
    suffix_array: Optional[
        List[int]
    ] = None,
) -> List[int]:
    """
    Construct the LCP array using Kasai's algorithm.

    lcp[i] is the longest common prefix between suffixes
    suffix_array[i] and suffix_array[i + 1].

    Complexity:
        O(n) time after suffix-array construction
        O(n) space
    """
    _validate_text(
        text
    )

    if suffix_array is None:
        suffix_array = build_suffix_array(
            text
        )
    else:
        _validate_suffix_array(
            text,
            suffix_array,
        )

    length = len(
        text
    )

    if length <= 1:
        return []

    rank = [
        0
    ] * length

    for position, suffix_start in enumerate(
        suffix_array
    ):
        rank[
            suffix_start
        ] = position

    lcp = [
        0
    ] * (
        length - 1
    )

    common_length = 0

    for text_index in range(
        length
    ):
        suffix_rank = rank[
            text_index
        ]

        if suffix_rank == length - 1:
            common_length = 0
            continue

        next_suffix = suffix_array[
            suffix_rank + 1
        ]

        while (
            text_index
            + common_length
            < length
            and next_suffix
            + common_length
            < length
            and text[
                text_index
                + common_length
            ]
            == text[
                next_suffix
                + common_length
            ]
        ):
            common_length += 1

        lcp[
            suffix_rank
        ] = common_length

        if common_length > 0:
            common_length -= 1

    return lcp


def _search_prevalidated_suffix_array(
    text: str,
    pattern: str,
    suffix_array: List[int],
) -> List[int]:
    """
    Search a known-valid suffix array.

    This helper intentionally skips suffix-array validation so
    reusable indexes do not pay O(n log n) validation cost on
    every query.
    """
    if pattern == "":
        return list(
            range(
                len(
                    text
                )
                + 1
            )
        )

    if len(
        pattern
    ) > len(
        text
    ):
        return []

    pattern_length = len(
        pattern
    )

    left = 0
    right = len(
        suffix_array
    )

    while left < right:
        middle = (
            left
            + right
        ) // 2

        suffix_start = suffix_array[
            middle
        ]

        prefix = text[
            suffix_start:
            suffix_start
            + pattern_length
        ]

        if prefix < pattern:
            left = middle + 1
        else:
            right = middle

    first = left

    left = first
    right = len(
        suffix_array
    )

    while left < right:
        middle = (
            left
            + right
        ) // 2

        suffix_start = suffix_array[
            middle
        ]

        prefix = text[
            suffix_start:
            suffix_start
            + pattern_length
        ]

        if prefix <= pattern:
            left = middle + 1
        else:
            right = middle

    last = left

    matches = [
        suffix_start
        for suffix_start in suffix_array[
            first:last
        ]
        if text.startswith(
            pattern,
            suffix_start,
        )
    ]

    return sorted(
        matches
    )


def suffix_array_search(
    text: str,
    pattern: str,
    suffix_array: Optional[
        List[int]
    ] = None,
) -> List[int]:
    """
    Find all occurrences of pattern using binary search over a suffix array.

    A caller-supplied suffix array is validated once for safety.
    Reusable SuffixArrayIndex objects bypass repeated validation.

    Returned match positions are sorted by their position in the text.
    """
    _validate_text(
        text
    )

    if not isinstance(
        pattern,
        str,
    ):
        raise TypeError(
            "pattern must be a string"
        )

    if suffix_array is None:
        suffix_array = build_suffix_array(
            text
        )
    else:
        _validate_suffix_array(
            text,
            suffix_array,
        )

    return _search_prevalidated_suffix_array(
        text,
        pattern,
        suffix_array,
    )


@dataclass
class SuffixArrayIndex:
    """Reusable suffix-array index for repeated substring queries."""

    text: str

    def __post_init__(
        self,
    ) -> None:
        _validate_text(
            self.text
        )

        self.suffix_array = build_suffix_array(
            self.text
        )

        self.lcp = build_lcp_array(
            self.text,
            self.suffix_array,
        )

    def find(
        self,
        pattern: str,
    ) -> List[int]:
        """Return all positions of pattern without rebuilding the index."""
        if not isinstance(
            pattern,
            str,
        ):
            raise TypeError(
                "pattern must be a string"
            )

        return _search_prevalidated_suffix_array(
            self.text,
            pattern,
            self.suffix_array,
        )

    def longest_repeated_substring(
        self,
    ) -> str:
        """Return one longest repeated substring."""
        if not self.lcp:
            return ""

        maximum = max(
            self.lcp
        )

        if maximum == 0:
            return ""

        lcp_index = self.lcp.index(
            maximum
        )

        start = self.suffix_array[
            lcp_index
        ]

        return self.text[
            start:
            start
            + maximum
        ]

    def distinct_substring_count(
        self,
    ) -> int:
        """Return the number of distinct nonempty substrings."""
        length = len(
            self.text
        )

        total_substrings = (
            length
            * (
                length + 1
            )
            // 2
        )

        return (
            total_substrings
            - sum(
                self.lcp
            )
        )