"""Unified interface for Week 11 string-search algorithms."""

from dataclasses import dataclass
from time import perf_counter
from typing import Dict, List, Optional

from StringSearchEngine.core.kmp import (
    kmp_search,
)
from StringSearchEngine.core.rabin_karp import (
    rabin_karp_search,
)
from StringSearchEngine.core.suffix_array import (
    SuffixArrayIndex,
)
from StringSearchEngine.core.suffix_tree import (
    CompressedSuffixTree,
)


SUPPORTED_METHODS = (
    "kmp",
    "rk",
    "sa",
    "tree",
)


@dataclass
class SearchResult:
    """One search result returned by StringSearchEngine."""

    pattern: str
    method: str
    positions: List[int]
    count: int
    search_time: float
    average_search_time: float
    preprocessing_time: float
    recommendation: str


class StringSearchEngine:
    """
    Unified interface for KMP, Rabin-Karp, suffix arrays,
    and compressed suffix trees.

    Indexed structures are created lazily. This avoids paying
    suffix-array or suffix-tree preprocessing cost unless that
    search method is actually requested.
    """

    def __init__(
        self,
        text: str,
    ) -> None:
        if not isinstance(
            text,
            str,
        ):
            raise TypeError(
                "text must be a string"
            )

        self.text = text

        self._suffix_array_index: Optional[
            SuffixArrayIndex
        ] = None

        self._suffix_tree: Optional[
            CompressedSuffixTree
        ] = None

        self._preprocessing_times = {
            "kmp": 0.0,
            "rk": 0.0,
            "sa": 0.0,
            "tree": 0.0,
        }

        self._search_times: Dict[
            str,
            List[float],
        ] = {
            method: []
            for method in SUPPORTED_METHODS
        }

    def _validate_method(
        self,
        method: str,
    ) -> str:
        """Validate and normalize a search-method name."""
        if not isinstance(
            method,
            str,
        ):
            raise TypeError(
                "method must be a string"
            )

        normalized = method.lower()

        if normalized not in SUPPORTED_METHODS:
            raise ValueError(
                "method must be one of: "
                "kmp, rk, sa, tree"
            )

        return normalized

    def _ensure_suffix_array(
        self,
    ) -> SuffixArrayIndex:
        """Build the suffix-array index once when first needed."""
        if self._suffix_array_index is None:
            start = perf_counter()

            self._suffix_array_index = (
                SuffixArrayIndex(
                    self.text
                )
            )

            self._preprocessing_times[
                "sa"
            ] = (
                perf_counter()
                - start
            )

        return self._suffix_array_index

    def _ensure_suffix_tree(
        self,
    ) -> CompressedSuffixTree:
        """Build the compressed suffix tree once when first needed."""
        if self._suffix_tree is None:
            start = perf_counter()

            self._suffix_tree = (
                CompressedSuffixTree(
                    self.text
                )
            )

            self._preprocessing_times[
                "tree"
            ] = (
                perf_counter()
                - start
            )

        return self._suffix_tree

    def preprocess(
        self,
        method: str,
    ) -> float:
        """
        Explicitly preprocess an indexed method.

        KMP and Rabin-Karp require no persistent index, so their
        preprocessing time remains zero.
        """
        normalized = self._validate_method(
            method
        )

        if normalized == "sa":
            self._ensure_suffix_array()

        elif normalized == "tree":
            self._ensure_suffix_tree()

        return self._preprocessing_times[
            normalized
        ]

    def _recommendation_for(
        self,
        method: str,
    ) -> str:
        """Return a short explanation of the selected method."""
        recommendations = {
            "kmp": (
                "KMP is a strong choice for deterministic "
                "single-pattern searches with linear worst-case time."
            ),
            "rk": (
                "Rabin-Karp is useful for fingerprint-based "
                "search and efficient multi-pattern extensions."
            ),
            "sa": (
                "Suffix arrays are effective when the same text "
                "will receive many substring queries."
            ),
            "tree": (
                "Suffix trees support fast repeated substring "
                "and prefix-oriented queries after preprocessing."
            ),
        }

        return recommendations[
            method
        ]

    def find(
        self,
        pattern: str,
        method: str = "kmp",
    ) -> SearchResult:
        """
        Search the engine text using one selected algorithm.

        Examples:
            engine.find("pattern", method="kmp")
            engine.find("pattern", method="rk")
            engine.find("pattern", method="sa")
            engine.find("pattern", method="tree")
        """
        if not isinstance(
            pattern,
            str,
        ):
            raise TypeError(
                "pattern must be a string"
            )

        normalized = self._validate_method(
            method
        )

        if normalized == "sa":
            index = self._ensure_suffix_array()

        elif normalized == "tree":
            tree = self._ensure_suffix_tree()

        start = perf_counter()

        if normalized == "kmp":
            positions = kmp_search(
                self.text,
                pattern,
            )

        elif normalized == "rk":
            positions = rabin_karp_search(
                self.text,
                pattern,
            )

        elif normalized == "sa":
            positions = index.find(
                pattern
            )

        else:
            positions = tree.find(
                pattern
            )

        elapsed = (
            perf_counter()
            - start
        )

        self._search_times[
            normalized
        ].append(
            elapsed
        )

        average = (
            sum(
                self._search_times[
                    normalized
                ]
            )
            / len(
                self._search_times[
                    normalized
                ]
            )
        )

        return SearchResult(
            pattern=pattern,
            method=normalized,
            positions=positions,
            count=len(
                positions
            ),
            search_time=elapsed,
            average_search_time=average,
            preprocessing_time=(
                self._preprocessing_times[
                    normalized
                ]
            ),
            recommendation=(
                self._recommendation_for(
                    normalized
                )
            ),
        )

    def find_all(
        self,
        pattern: str,
    ) -> Dict[
        str,
        SearchResult,
    ]:
        """Search for one pattern using all four algorithms."""
        return {
            method: self.find(
                pattern,
                method=method,
            )
            for method in SUPPORTED_METHODS
        }

    def statistics(
        self,
    ) -> Dict[
        str,
        Dict[str, float],
    ]:
        """Return query and preprocessing statistics by method."""
        results = {}

        for method in SUPPORTED_METHODS:
            times = self._search_times[
                method
            ]

            average = (
                sum(
                    times
                )
                / len(
                    times
                )
                if times
                else 0.0
            )

            results[
                method
            ] = {
                "queries": len(
                    times
                ),
                "average_search_time": average,
                "preprocessing_time": (
                    self._preprocessing_times[
                        method
                    ]
                ),
            }

        return results

    def recommend_method(
        self,
        repeated_queries: bool = False,
        multiple_patterns: bool = False,
        prefix_queries: bool = False,
    ) -> str:
        """Recommend a method based on a simple usage scenario."""
        if not isinstance(
            repeated_queries,
            bool,
        ):
            raise TypeError(
                "repeated_queries must be boolean"
            )

        if not isinstance(
            multiple_patterns,
            bool,
        ):
            raise TypeError(
                "multiple_patterns must be boolean"
            )

        if not isinstance(
            prefix_queries,
            bool,
        ):
            raise TypeError(
                "prefix_queries must be boolean"
            )

        if prefix_queries:
            return "tree"

        if multiple_patterns:
            return "rk"

        if repeated_queries:
            return "sa"

        return "kmp"