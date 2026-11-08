"""Compressed suffix trie for substring indexing."""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class SuffixTreeNode:
    """One node in the compressed suffix trie."""

    edges: Dict[
        str,
        "SuffixTreeEdge",
    ] = field(
        default_factory=dict
    )

    terminal_starts: List[int] = field(
        default_factory=list
    )


@dataclass
class SuffixTreeEdge:
    """A compressed edge labeled with one or more characters."""

    label: str
    child: SuffixTreeNode


def _common_prefix_length(
    first: str,
    second: str,
) -> int:
    """Return the common-prefix length of two strings."""
    limit = min(
        len(
            first
        ),
        len(
            second
        ),
    )

    index = 0

    while (
        index < limit
        and first[
            index
        ]
        == second[
            index
        ]
    ):
        index += 1

    return index


@dataclass
class CompressedSuffixTree:
    """
    Compressed suffix trie built by inserting every suffix.

    This is the assignment's Option A implementation. It uses
    path compression rather than Ukkonen's online construction.

    Construction is simple and appropriate for demonstrating
    suffix-tree behavior, though its worst-case build cost is
    quadratic because all suffixes are inserted explicitly.
    """

    text: str

    def __post_init__(
        self,
    ) -> None:
        if not isinstance(
            self.text,
            str,
        ):
            raise TypeError(
                "text must be a string"
            )

        self.root = SuffixTreeNode()

        for start in range(
            len(
                self.text
            )
        ):
            self._insert_suffix(
                self.text[
                    start:
                ],
                start,
            )

    def _insert_suffix(
        self,
        suffix: str,
        start: int,
    ) -> None:
        """Insert one suffix into the compressed trie."""
        node = self.root
        remaining = suffix

        while remaining:
            first_character = remaining[
                0
            ]

            edge = node.edges.get(
                first_character
            )

            if edge is None:
                leaf = SuffixTreeNode(
                    terminal_starts=[
                        start
                    ]
                )

                node.edges[
                    first_character
                ] = SuffixTreeEdge(
                    label=remaining,
                    child=leaf,
                )

                return

            common_length = _common_prefix_length(
                remaining,
                edge.label,
            )

            if common_length == len(
                edge.label
            ):
                remaining = remaining[
                    common_length:
                ]

                node = edge.child

                if not remaining:
                    node.terminal_starts.append(
                        start
                    )

                    return

                continue

            shared_label = edge.label[
                :common_length
            ]

            old_remainder = edge.label[
                common_length:
            ]

            new_remainder = remaining[
                common_length:
            ]

            split_node = SuffixTreeNode()

            node.edges[
                first_character
            ] = SuffixTreeEdge(
                label=shared_label,
                child=split_node,
            )

            split_node.edges[
                old_remainder[
                    0
                ]
            ] = SuffixTreeEdge(
                label=old_remainder,
                child=edge.child,
            )

            if new_remainder:
                new_leaf = SuffixTreeNode(
                    terminal_starts=[
                        start
                    ]
                )

                split_node.edges[
                    new_remainder[
                        0
                    ]
                ] = SuffixTreeEdge(
                    label=new_remainder,
                    child=new_leaf,
                )
            else:
                split_node.terminal_starts.append(
                    start
                )

            return

    def _collect_suffix_starts(
        self,
        node: SuffixTreeNode,
    ) -> List[int]:
        """Collect suffix starts below one node."""
        starts = list(
            node.terminal_starts
        )

        for edge in node.edges.values():
            starts.extend(
                self._collect_suffix_starts(
                    edge.child
                )
            )

        return starts

    def find(
        self,
        pattern: str,
    ) -> List[int]:
        """
        Return all starting positions of pattern in the text.

        The search follows compressed edge labels rather than
        scanning the original text from every position.
        """
        if not isinstance(
            pattern,
            str,
        ):
            raise TypeError(
                "pattern must be a string"
            )

        if pattern == "":
            return list(
                range(
                    len(
                        self.text
                    )
                    + 1
                )
            )

        if len(
            pattern
        ) > len(
            self.text
        ):
            return []

        node = self.root
        remaining = pattern

        while remaining:
            edge = node.edges.get(
                remaining[
                    0
                ]
            )

            if edge is None:
                return []

            common_length = _common_prefix_length(
                remaining,
                edge.label,
            )

            if common_length == len(
                remaining
            ):
                return sorted(
                    self._collect_suffix_starts(
                        edge.child
                    )
                )

            if common_length < len(
                edge.label
            ):
                return []

            remaining = remaining[
                common_length:
            ]

            node = edge.child

        return sorted(
            self._collect_suffix_starts(
                node
            )
        )

    def contains(
        self,
        pattern: str,
    ) -> bool:
        """Return True when pattern occurs in the text."""
        return bool(
            self.find(
                pattern
            )
        ) or pattern == ""

    def prefix_matches(
        self,
        prefix: str,
    ) -> List[int]:
        """
        Return suffix starts whose suffix begins with prefix.

        For a suffix tree, this is equivalent to locating all
        occurrences of the prefix in the original text.
        """
        if not isinstance(
            prefix,
            str,
        ):
            raise TypeError(
                "prefix must be a string"
            )

        return self.find(
            prefix
        )

    def longest_repeated_substring(
        self,
    ) -> str:
        """
        Return one longest substring appearing at least twice.

        Overlapping repetitions are allowed.
        """
        best = ""

        def visit(
            node: SuffixTreeNode,
            path: str,
        ) -> int:
            nonlocal best

            total_suffixes = len(
                node.terminal_starts
            )

            for edge in node.edges.values():
                child_path = (
                    path
                    + edge.label
                )

                child_count = visit(
                    edge.child,
                    child_path,
                )

                total_suffixes += child_count

            if (
                total_suffixes >= 2
                and len(
                    path
                )
                > len(
                    best
                )
            ):
                best = path

            return total_suffixes

        visit(
            self.root,
            "",
        )

        return best

    def distinct_substring_count(
        self,
    ) -> int:
        """
        Count distinct nonempty substrings.

        Each character position along a compressed tree edge
        represents one distinct prefix of a suffix.
        """
        total = 0

        stack = [
            self.root
        ]

        while stack:
            node = stack.pop()

            for edge in node.edges.values():
                total += len(
                    edge.label
                )

                stack.append(
                    edge.child
                )

        return total

    def statistics(
        self,
    ) -> Dict[str, int]:
        """Return simple structural statistics for the tree."""
        node_count = 0
        edge_count = 0
        terminal_count = 0

        stack = [
            self.root
        ]

        while stack:
            node = stack.pop()

            node_count += 1

            terminal_count += len(
                node.terminal_starts
            )

            for edge in node.edges.values():
                edge_count += 1

                stack.append(
                    edge.child
                )

        return {
            "nodes": node_count,
            "edges": edge_count,
            "suffixes": terminal_count,
        }

    def edge_records(
        self,
    ) -> List[
        Tuple[
            int,
            int,
            str,
        ]
    ]:
        """
        Return numbered parent-child edge records.

        This representation is useful for later visualization.
        """
        records = []

        queue = [
            (
                self.root,
                0,
            )
        ]

        next_identifier = 1

        while queue:
            node, parent_identifier = queue.pop(
                0
            )

            for key in sorted(
                node.edges
            ):
                edge = node.edges[
                    key
                ]

                child_identifier = next_identifier

                next_identifier += 1

                records.append(
                    (
                        parent_identifier,
                        child_identifier,
                        edge.label,
                    )
                )

                queue.append(
                    (
                        edge.child,
                        child_identifier,
                    )
                )

        return records


SuffixTree = CompressedSuffixTree