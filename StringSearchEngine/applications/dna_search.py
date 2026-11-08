"""DNA sequence search using suffix arrays and compressed suffix trees."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from StringSearchEngine.core.suffix_array import (
    SuffixArrayIndex,
)
from StringSearchEngine.core.suffix_tree import (
    CompressedSuffixTree,
)


VALID_DNA_CHARACTERS = {
    "A",
    "C",
    "G",
    "T",
    "N",
}


@dataclass
class FASTARecord:
    """One FASTA record."""

    header: str
    sequence: str


@dataclass
class DNASearchResult:
    """Result of one DNA substring query."""

    pattern: str
    method: str
    positions: List[int]
    count: int


def normalize_dna(
    sequence: str,
) -> str:
    """
    Normalize a DNA sequence.

    Whitespace is removed and letters are converted to uppercase.
    A, C, G, T, and N are accepted.
    """
    if not isinstance(
        sequence,
        str,
    ):
        raise TypeError(
            "sequence must be a string"
        )

    normalized = "".join(
        sequence.split()
    ).upper()

    invalid = {
        character
        for character in normalized
        if character not in VALID_DNA_CHARACTERS
    }

    if invalid:
        raise ValueError(
            "sequence contains invalid DNA characters: "
            + ", ".join(
                sorted(
                    invalid
                )
            )
        )

    return normalized


def parse_fasta(
    fasta_text: str,
) -> List[FASTARecord]:
    """Parse FASTA-formatted text into records."""
    if not isinstance(
        fasta_text,
        str,
    ):
        raise TypeError(
            "fasta_text must be a string"
        )

    if not fasta_text.strip():
        return []

    records = []

    current_header: Optional[str] = None
    sequence_lines = []

    for raw_line in fasta_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith(
            ">"
        ):
            if current_header is not None:
                records.append(
                    FASTARecord(
                        header=current_header,
                        sequence=normalize_dna(
                            "".join(
                                sequence_lines
                            )
                        ),
                    )
                )

            current_header = line[
                1:
            ].strip()

            if not current_header:
                raise ValueError(
                    "FASTA header must not be empty"
                )

            sequence_lines = []

        else:
            if current_header is None:
                raise ValueError(
                    "FASTA sequence encountered before header"
                )

            sequence_lines.append(
                line
            )

    if current_header is not None:
        records.append(
            FASTARecord(
                header=current_header,
                sequence=normalize_dna(
                    "".join(
                        sequence_lines
                    )
                ),
            )
        )

    return records


def load_fasta(
    path: str | Path,
) -> List[FASTARecord]:
    """Load and parse a FASTA file."""
    file_path = Path(
        path
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"FASTA file not found: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            "FASTA path must refer to a file"
        )

    text = file_path.read_text(
        encoding="utf-8"
    )

    return parse_fasta(
        text
    )


class DNASequenceSearch:
    """
    Search one DNA sequence using suffix-array or suffix-tree indexing.

    The suffix tree is built lazily because the compressed-trie
    implementation is intended for smaller demonstration datasets.
    """

    def __init__(
        self,
        sequence: str,
    ) -> None:
        self.sequence = normalize_dna(
            sequence
        )

        self._suffix_array = SuffixArrayIndex(
            self.sequence
        )

        self._suffix_tree: Optional[
            CompressedSuffixTree
        ] = None

    def _ensure_tree(
        self,
    ) -> CompressedSuffixTree:
        """Build the compressed suffix tree when first requested."""
        if self._suffix_tree is None:
            self._suffix_tree = (
                CompressedSuffixTree(
                    self.sequence
                )
            )

        return self._suffix_tree

    def find(
        self,
        pattern: str,
        method: str = "sa",
    ) -> DNASearchResult:
        """Find all exact occurrences of a DNA pattern."""
        normalized_pattern = normalize_dna(
            pattern
        )

        if not isinstance(
            method,
            str,
        ):
            raise TypeError(
                "method must be a string"
            )

        normalized_method = method.lower()

        if normalized_method == "sa":
            positions = self._suffix_array.find(
                normalized_pattern
            )

        elif normalized_method == "tree":
            positions = self._ensure_tree().find(
                normalized_pattern
            )

        else:
            raise ValueError(
                "method must be 'sa' or 'tree'"
            )

        return DNASearchResult(
            pattern=normalized_pattern,
            method=normalized_method,
            positions=positions,
            count=len(
                positions
            ),
        )

    def find_many(
        self,
        patterns: List[str],
        method: str = "sa",
    ) -> Dict[
        str,
        DNASearchResult,
    ]:
        """Search multiple DNA patterns."""
        if not isinstance(
            patterns,
            list,
        ):
            raise TypeError(
                "patterns must be a list"
            )

        results = {}

        for pattern in patterns:
            if not isinstance(
                pattern,
                str,
            ):
                raise TypeError(
                    "every pattern must be a string"
                )

            result = self.find(
                pattern,
                method=method,
            )

            results[
                result.pattern
            ] = result

        return results

    def longest_repeated_sequence(
        self,
        method: str = "sa",
    ) -> str:
        """Return a longest repeated DNA substring."""
        if not isinstance(
            method,
            str,
        ):
            raise TypeError(
                "method must be a string"
            )

        normalized_method = method.lower()

        if normalized_method == "sa":
            return (
                self._suffix_array
                .longest_repeated_substring()
            )

        if normalized_method == "tree":
            return (
                self._ensure_tree()
                .longest_repeated_substring()
            )

        raise ValueError(
            "method must be 'sa' or 'tree'"
        )


def search_fasta_records(
    records: List[FASTARecord],
    pattern: str,
    method: str = "sa",
) -> Dict[
    str,
    DNASearchResult,
]:
    """Search one DNA pattern across multiple FASTA records."""
    if not isinstance(
        records,
        list,
    ):
        raise TypeError(
            "records must be a list"
        )

    results = {}

    for record in records:
        if not isinstance(
            record,
            FASTARecord,
        ):
            raise TypeError(
                "records must contain FASTARecord objects"
            )

        searcher = DNASequenceSearch(
            record.sequence
        )

        results[
            record.header
        ] = searcher.find(
            pattern,
            method=method,
        )

    return results