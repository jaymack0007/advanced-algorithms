"""Rabin-Karp string matching with collision tracking."""

from dataclasses import dataclass
from typing import Dict, List, Sequence

from StringSearchEngine.utils.rolling_hash import (
    DEFAULT_BASE,
    DEFAULT_MODULUS,
    RollingHash,
    polynomial_hash,
)


@dataclass
class RabinKarpResult:
    """Detailed result for one Rabin-Karp pattern search."""

    matches: List[int]
    hash_hits: int
    collisions: int
    windows_checked: int
    base: int
    modulus: int


def rabin_karp_search_with_stats(
    text: str,
    pattern: str,
    base: int = DEFAULT_BASE,
    modulus: int = DEFAULT_MODULUS,
) -> RabinKarpResult:
    """
    Search for all occurrences of a pattern using Rabin-Karp.

    A hash hit is verified with direct string comparison so the
    returned match positions are always exact even if collisions
    occur.

    Expected complexity:
        O(n + m)

    Worst-case complexity:
        O(nm)
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
        return RabinKarpResult(
            matches=list(
                range(
                    len(
                        text
                    )
                    + 1
                )
            ),
            hash_hits=0,
            collisions=0,
            windows_checked=0,
            base=base,
            modulus=modulus,
        )

    if len(
        pattern
    ) > len(
        text
    ):
        return RabinKarpResult(
            matches=[],
            hash_hits=0,
            collisions=0,
            windows_checked=0,
            base=base,
            modulus=modulus,
        )

    pattern_hash = polynomial_hash(
        pattern,
        base=base,
        modulus=modulus,
    )

    window = text[
        :len(
            pattern
        )
    ]

    rolling = RollingHash(
        window,
        base=base,
        modulus=modulus,
    )

    matches = []
    hash_hits = 0
    collisions = 0
    windows_checked = 0

    last_start = (
        len(
            text
        )
        - len(
            pattern
        )
    )

    for start in range(
        last_start + 1
    ):
        windows_checked += 1

        if rolling.value == pattern_hash:
            hash_hits += 1

            candidate = text[
                start:
                start
                + len(
                    pattern
                )
            ]

            if candidate == pattern:
                matches.append(
                    start
                )
            else:
                collisions += 1

        if start < last_start:
            rolling.slide(
                text[
                    start
                ],
                text[
                    start
                    + len(
                        pattern
                    )
                ],
            )

    return RabinKarpResult(
        matches=matches,
        hash_hits=hash_hits,
        collisions=collisions,
        windows_checked=windows_checked,
        base=base,
        modulus=modulus,
    )


def rabin_karp_search(
    text: str,
    pattern: str,
    base: int = DEFAULT_BASE,
    modulus: int = DEFAULT_MODULUS,
) -> List[int]:
    """Return exact match positions using Rabin-Karp."""
    return rabin_karp_search_with_stats(
        text,
        pattern,
        base=base,
        modulus=modulus,
    ).matches


def rabin_karp_multi_search(
    text: str,
    patterns: Sequence[str],
    base: int = DEFAULT_BASE,
    modulus: int = DEFAULT_MODULUS,
) -> Dict[
    str,
    List[int],
]:
    """
    Search for multiple patterns.

    Patterns are grouped by length so windows of the same size
    share one rolling scan of the input text.
    """
    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string"
        )

    if not isinstance(
        patterns,
        (list, tuple),
    ):
        raise TypeError(
            "patterns must be a list or tuple"
        )

    for pattern in patterns:
        if not isinstance(
            pattern,
            str,
        ):
            raise TypeError(
                "every pattern must be a string"
            )

    unique_patterns = list(
        dict.fromkeys(
            patterns
        )
    )

    results = {
        pattern: []
        for pattern in unique_patterns
    }

    if not unique_patterns:
        return results

    for pattern in unique_patterns:
        if pattern == "":
            results[
                pattern
            ] = list(
                range(
                    len(
                        text
                    )
                    + 1
                )
            )

    groups = {}

    for pattern in unique_patterns:
        if not pattern:
            continue

        if len(
            pattern
        ) > len(
            text
        ):
            continue

        groups.setdefault(
            len(
                pattern
            ),
            [],
        ).append(
            pattern
        )

    for pattern_length, group in groups.items():
        hashes = {}

        for pattern in group:
            value = polynomial_hash(
                pattern,
                base=base,
                modulus=modulus,
            )

            hashes.setdefault(
                value,
                [],
            ).append(
                pattern
            )

        rolling = RollingHash(
            text[
                :pattern_length
            ],
            base=base,
            modulus=modulus,
        )

        last_start = (
            len(
                text
            )
            - pattern_length
        )

        for start in range(
            last_start + 1
        ):
            candidates = hashes.get(
                rolling.value,
                [],
            )

            if candidates:
                window = text[
                    start:
                    start
                    + pattern_length
                ]

                for pattern in candidates:
                    if window == pattern:
                        results[
                            pattern
                        ].append(
                            start
                        )

            if start < last_start:
                rolling.slide(
                    text[
                        start
                    ],
                    text[
                        start
                        + pattern_length
                    ],
                )

    return results