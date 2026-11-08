"""Synthetic text generators for Week 11 testing and benchmarks."""

import random
import string
from typing import List, Sequence


DEFAULT_ALPHABET = (
    string.ascii_lowercase
    + " "
)

DNA_ALPHABET = "ACGT"


def _validate_length(
    length: int,
) -> None:
    """Validate a requested generated length."""
    if (
        isinstance(
            length,
            bool,
        )
        or not isinstance(
            length,
            int,
        )
    ):
        raise TypeError(
            "length must be an integer"
        )

    if length < 0:
        raise ValueError(
            "length must be non-negative"
        )


def random_text(
    length: int,
    alphabet: str = DEFAULT_ALPHABET,
    seed: int | None = None,
) -> str:
    """Generate deterministic pseudo-random text when a seed is supplied."""
    _validate_length(
        length
    )

    if not isinstance(
        alphabet,
        str,
    ):
        raise TypeError(
            "alphabet must be a string"
        )

    if not alphabet:
        raise ValueError(
            "alphabet must not be empty"
        )

    if (
        seed is not None
        and (
            isinstance(
                seed,
                bool,
            )
            or not isinstance(
                seed,
                int,
            )
        )
    ):
        raise TypeError(
            "seed must be an integer or None"
        )

    generator = random.Random(
        seed
    )

    return "".join(
        generator.choice(
            alphabet
        )
        for _ in range(
            length
        )
    )


def repetitive_text(
    length: int,
    pattern: str = "abcde",
) -> str:
    """Generate text by repeating a fixed pattern."""
    _validate_length(
        length
    )

    if not isinstance(
        pattern,
        str,
    ):
        raise TypeError(
            "pattern must be a string"
        )

    if not pattern:
        raise ValueError(
            "pattern must not be empty"
        )

    repeats = (
        length
        // len(
            pattern
        )
        + 1
    )

    return (
        pattern
        * repeats
    )[
        :length
    ]


def random_dna(
    length: int,
    seed: int | None = None,
    include_n: bool = False,
) -> str:
    """Generate a pseudo-random DNA sequence."""
    if not isinstance(
        include_n,
        bool,
    ):
        raise TypeError(
            "include_n must be boolean"
        )

    alphabet = (
        DNA_ALPHABET
        + (
            "N"
            if include_n
            else ""
        )
    )

    return random_text(
        length,
        alphabet=alphabet,
        seed=seed,
    )


def embed_pattern(
    text: str,
    pattern: str,
    positions: Sequence[int],
) -> str:
    """
    Insert a fixed-length pattern at selected positions.

    Existing characters are replaced, so the total text length
    remains unchanged.
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

    if not pattern:
        raise ValueError(
            "pattern must not be empty"
        )

    if not isinstance(
        positions,
        (list, tuple),
    ):
        raise TypeError(
            "positions must be a list or tuple"
        )

    result = list(
        text
    )

    for position in positions:
        if (
            isinstance(
                position,
                bool,
            )
            or not isinstance(
                position,
                int,
            )
        ):
            raise TypeError(
                "positions must contain integers"
            )

        if (
            position < 0
            or position
            + len(
                pattern
            )
            > len(
                text
            )
        ):
            raise ValueError(
                "pattern position is outside text bounds"
            )

        result[
            position:
            position
            + len(
                pattern
            )
        ] = list(
            pattern
        )

    return "".join(
        result
    )


def sample_patterns(
    text: str,
    pattern_length: int,
    count: int,
    seed: int | None = None,
) -> List[str]:
    """Sample substring patterns from existing text."""
    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string"
        )

    _validate_length(
        pattern_length
    )

    _validate_length(
        count
    )

    if pattern_length == 0:
        raise ValueError(
            "pattern_length must be positive"
        )

    if pattern_length > len(
        text
    ):
        raise ValueError(
            "pattern_length cannot exceed text length"
        )

    available_starts = (
        len(
            text
        )
        - pattern_length
        + 1
    )

    if count > available_starts:
        raise ValueError(
            "count exceeds available substring starts"
        )

    if (
        seed is not None
        and (
            isinstance(
                seed,
                bool,
            )
            or not isinstance(
                seed,
                int,
            )
        )
    ):
        raise TypeError(
            "seed must be an integer or None"
        )

    generator = random.Random(
        seed
    )

    starts = generator.sample(
        range(
            available_starts
        ),
        count,
    )

    return [
        text[
            start:
            start
            + pattern_length
        ]
        for start in starts
    ]