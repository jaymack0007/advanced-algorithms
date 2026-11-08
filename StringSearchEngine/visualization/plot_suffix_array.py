"""Suffix-array and LCP visualization utilities."""

from pathlib import Path
from typing import List, Optional

import matplotlib

matplotlib.use(
    "Agg"
)

import matplotlib.pyplot as plt

from StringSearchEngine.core.suffix_array import (
    build_lcp_array,
    build_suffix_array,
)


def suffix_table(
    text: str,
    suffix_array: Optional[
        List[int]
    ] = None,
    lcp: Optional[
        List[int]
    ] = None,
) -> List[dict]:
    """Return suffix-array rows for display or analysis."""
    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string"
        )

    if suffix_array is None:
        suffix_array = build_suffix_array(
            text
        )

    if lcp is None:
        lcp = build_lcp_array(
            text,
            suffix_array,
        )

    rows = []

    for rank, start in enumerate(
        suffix_array
    ):
        rows.append(
            {
                "rank": rank,
                "start": start,
                "suffix": text[
                    start:
                ],
                "lcp_next": (
                    lcp[
                        rank
                    ]
                    if rank < len(
                        lcp
                    )
                    else 0
                ),
            }
        )

    return rows


def plot_suffix_array(
    text: str,
    output_path: str | Path,
    max_suffixes: int = 30,
    show: bool = False,
) -> Path:
    """
    Plot suffix-array positions and LCP values.

    The first max_suffixes lexicographically sorted suffixes are shown.
    """
    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string"
        )

    if (
        isinstance(
            max_suffixes,
            bool,
        )
        or not isinstance(
            max_suffixes,
            int,
        )
    ):
        raise TypeError(
            "max_suffixes must be an integer"
        )

    if max_suffixes <= 0:
        raise ValueError(
            "max_suffixes must be positive"
        )

    if not isinstance(
        show,
        bool,
    ):
        raise TypeError(
            "show must be boolean"
        )

    output = Path(
        output_path
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    suffix_array = build_suffix_array(
        text
    )

    lcp = build_lcp_array(
        text,
        suffix_array,
    )

    displayed_count = min(
        len(
            suffix_array
        ),
        max_suffixes,
    )

    displayed_sa = suffix_array[
        :displayed_count
    ]

    displayed_lcp = [
        (
            lcp[
                index
            ]
            if index < len(
                lcp
            )
            else 0
        )
        for index in range(
            displayed_count
        )
    ]

    ranks = list(
        range(
            displayed_count
        )
    )

    figure, axes = plt.subplots(
        2,
        1,
        figsize=(
            10,
            7,
        ),
    )

    axes[
        0
    ].bar(
        ranks,
        displayed_sa,
    )

    axes[
        0
    ].set_title(
        "Suffix Array Positions"
    )

    axes[
        0
    ].set_xlabel(
        "Suffix Rank"
    )

    axes[
        0
    ].set_ylabel(
        "Text Start Position"
    )

    axes[
        1
    ].bar(
        ranks,
        displayed_lcp,
    )

    axes[
        1
    ].set_title(
        "LCP Values"
    )

    axes[
        1
    ].set_xlabel(
        "Suffix Rank"
    )

    axes[
        1
    ].set_ylabel(
        "Common Prefix Length"
    )

    figure.tight_layout()

    figure.savefig(
        output,
        dpi=150,
        bbox_inches="tight",
    )

    if show:
        plt.show()

    plt.close(
        figure
    )

    return output