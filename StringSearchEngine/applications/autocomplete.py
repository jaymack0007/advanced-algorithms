"""Prefix-based autocomplete with frequency weighting."""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple


@dataclass
class AutocompleteSuggestion:
    """One autocomplete suggestion."""

    term: str
    frequency: int


class AutocompleteEngine:
    """
    Prefix-based autocomplete engine.

    Terms are indexed by every nonempty prefix. Suggestions are
    ranked by descending frequency, then alphabetically.
    """

    def __init__(
        self,
        terms: Iterable[
            Tuple[
                str,
                int,
            ]
        ],
        case_sensitive: bool = False,
    ) -> None:
        if not isinstance(
            case_sensitive,
            bool,
        ):
            raise TypeError(
                "case_sensitive must be boolean"
            )

        if not isinstance(
            terms,
            (list, tuple),
        ):
            raise TypeError(
                "terms must be a list or tuple"
            )

        self.case_sensitive = case_sensitive

        self._frequencies: Dict[
            str,
            int,
        ] = {}

        self._display_terms: Dict[
            str,
            str,
        ] = {}

        for item in terms:
            if not isinstance(
                item,
                tuple,
            ):
                raise TypeError(
                    "each term entry must be a tuple"
                )

            if len(
                item
            ) != 2:
                raise ValueError(
                    "each term entry must contain term and frequency"
                )

            term, frequency = item

            if not isinstance(
                term,
                str,
            ):
                raise TypeError(
                    "term must be a string"
                )

            if not term:
                raise ValueError(
                    "term must not be empty"
                )

            if (
                isinstance(
                    frequency,
                    bool,
                )
                or not isinstance(
                    frequency,
                    int,
                )
            ):
                raise TypeError(
                    "frequency must be an integer"
                )

            if frequency < 0:
                raise ValueError(
                    "frequency must be non-negative"
                )

            key = self._normalize(
                term
            )

            self._frequencies[
                key
            ] = (
                self._frequencies.get(
                    key,
                    0,
                )
                + frequency
            )

            self._display_terms[
                key
            ] = term

        self._prefix_index: Dict[
            str,
            List[str],
        ] = {}

        self._build_index()

    def _normalize(
        self,
        value: str,
    ) -> str:
        """Normalize terms and prefixes."""
        if self.case_sensitive:
            return value

        return value.lower()

    def _build_index(
        self,
    ) -> None:
        """Build prefix-to-term lookup lists."""
        for key in self._frequencies:
            for length in range(
                1,
                len(
                    key
                )
                + 1,
            ):
                prefix = key[
                    :length
                ]

                self._prefix_index.setdefault(
                    prefix,
                    [],
                ).append(
                    key
                )

        for prefix in self._prefix_index:
            self._prefix_index[
                prefix
            ].sort(
                key=lambda key: (
                    -self._frequencies[
                        key
                    ],
                    self._display_terms[
                        key
                    ].lower(),
                    self._display_terms[
                        key
                    ],
                )
            )

    def add(
        self,
        term: str,
        frequency: int = 1,
    ) -> None:
        """Add a term or increase its frequency."""
        if not isinstance(
            term,
            str,
        ):
            raise TypeError(
                "term must be a string"
            )

        if not term:
            raise ValueError(
                "term must not be empty"
            )

        if (
            isinstance(
                frequency,
                bool,
            )
            or not isinstance(
                frequency,
                int,
            )
        ):
            raise TypeError(
                "frequency must be an integer"
            )

        if frequency < 0:
            raise ValueError(
                "frequency must be non-negative"
            )

        key = self._normalize(
            term
        )

        self._frequencies[
            key
        ] = (
            self._frequencies.get(
                key,
                0,
            )
            + frequency
        )

        self._display_terms[
            key
        ] = term

        self._prefix_index = {}

        self._build_index()

    def autocomplete(
        self,
        prefix: str,
        top_k: int = 5,
    ) -> List[AutocompleteSuggestion]:
        """
        Return the highest-ranked completions for a prefix.

        Ranking:
            1. Higher frequency first
            2. Alphabetical order for ties
        """
        if not isinstance(
            prefix,
            str,
        ):
            raise TypeError(
                "prefix must be a string"
            )

        if (
            isinstance(
                top_k,
                bool,
            )
            or not isinstance(
                top_k,
                int,
            )
        ):
            raise TypeError(
                "top_k must be an integer"
            )

        if top_k < 0:
            raise ValueError(
                "top_k must be non-negative"
            )

        if top_k == 0:
            return []

        normalized_prefix = self._normalize(
            prefix
        )

        if normalized_prefix == "":
            keys = sorted(
                self._frequencies,
                key=lambda key: (
                    -self._frequencies[
                        key
                    ],
                    self._display_terms[
                        key
                    ].lower(),
                    self._display_terms[
                        key
                    ],
                ),
            )
        else:
            keys = self._prefix_index.get(
                normalized_prefix,
                [],
            )

        return [
            AutocompleteSuggestion(
                term=self._display_terms[
                    key
                ],
                frequency=self._frequencies[
                    key
                ],
            )
            for key in keys[
                :top_k
            ]
        ]

    def record_query(
        self,
        term: str,
        amount: int = 1,
    ) -> None:
        """Increase a term's frequency based on observed use."""
        self.add(
            term,
            frequency=amount,
        )

    def frequency(
        self,
        term: str,
    ) -> int:
        """Return the current frequency of a term."""
        if not isinstance(
            term,
            str,
        ):
            raise TypeError(
                "term must be a string"
            )

        key = self._normalize(
            term
        )

        return self._frequencies.get(
            key,
            0,
        )

    def vocabulary_size(
        self,
    ) -> int:
        """Return the number of unique indexed terms."""
        return len(
            self._frequencies
        )