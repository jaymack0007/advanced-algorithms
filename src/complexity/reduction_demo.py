"""Demonstration of a polynomial-time reduction from 3-SAT to Vertex Cover."""

from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, List, Set, Tuple


Edge = Tuple[str, str]
Clause = Tuple[str, str, str]


@dataclass
class ReductionResult:
    """Container for a 3-SAT to Vertex Cover reduction."""

    vertices: Set[str]
    edges: List[Edge]
    target_size: int
    variables: List[str]
    clauses: List[Clause]
    clause_vertices: List[List[str]]
    steps: List[str]


def literal_variable(
    literal: str,
) -> str:
    """Return the variable name from a literal."""
    if literal.startswith("~"):
        return literal[1:]

    return literal


def literal_is_positive(
    literal: str,
) -> bool:
    """Return True when the literal is positive."""
    return not literal.startswith("~")


def evaluate_literal(
    literal: str,
    assignment: Dict[str, bool],
) -> bool:
    """Evaluate one literal under an assignment."""
    variable = literal_variable(
        literal
    )

    value = assignment[
        variable
    ]

    if literal_is_positive(
        literal
    ):
        return value

    return not value


def evaluate_formula(
    clauses: Iterable[Clause],
    assignment: Dict[str, bool],
) -> bool:
    """Return whether every clause is satisfied."""
    return all(
        any(
            evaluate_literal(
                literal,
                assignment,
            )
            for literal in clause
        )
        for clause in clauses
    )


def reduce_3sat_to_vertex_cover(
    clauses: List[Clause],
) -> ReductionResult:
    """
    Reduce a 3-SAT instance to Vertex Cover.

    Construction:
    1. Create two vertices for each variable: x and ~x.
    2. Connect each variable pair.
    3. Create a triangle for every three-literal clause.
    4. Connect each clause occurrence to its matching literal vertex.
    5. Set k = n + 2m.
    """
    if not clauses:
        raise ValueError(
            "clauses must not be empty"
        )

    for clause in clauses:
        if len(clause) != 3:
            raise ValueError(
                "each clause must contain exactly three literals"
            )

    variables = sorted(
        {
            literal_variable(
                literal
            )
            for clause in clauses
            for literal in clause
        }
    )

    vertices: Set[str] = set()
    edges: List[Edge] = []
    clause_vertices: List[List[str]] = []
    steps: List[str] = []

    steps.append(
        "Step 1: Create one variable pair for each variable."
    )

    for variable in variables:
        positive = variable
        negative = f"~{variable}"

        vertices.add(
            positive
        )
        vertices.add(
            negative
        )

        edges.append(
            (
                positive,
                negative,
            )
        )

        steps.append(
            f"  Added variable edge ({positive}, {negative})."
        )

    steps.append(
        "Step 2: Create one triangle for each clause."
    )

    for clause_index, clause in enumerate(
        clauses,
        start=1,
    ):
        occurrence_vertices = []

        for literal_index, literal in enumerate(
            clause,
            start=1,
        ):
            vertex = (
                f"C{clause_index}_"
                f"{literal_index}:"
                f"{literal}"
            )

            vertices.add(
                vertex
            )

            occurrence_vertices.append(
                vertex
            )

        clause_vertices.append(
            occurrence_vertices
        )

        for first, second in combinations(
            occurrence_vertices,
            2,
        ):
            edges.append(
                (
                    first,
                    second,
                )
            )

        steps.append(
            f"  Clause {clause_index} {clause} "
            "became a three-vertex triangle."
        )

    steps.append(
        "Step 3: Connect clause literals to matching variable literals."
    )

    for clause_index, clause in enumerate(
        clauses
    ):
        for literal_index, literal in enumerate(
            clause
        ):
            occurrence_vertex = (
                clause_vertices[
                    clause_index
                ][
                    literal_index
                ]
            )

            edges.append(
                (
                    occurrence_vertex,
                    literal,
                )
            )

            steps.append(
                f"  Connected {occurrence_vertex} "
                f"to {literal}."
            )

    target_size = (
        len(variables)
        + 2 * len(clauses)
    )

    steps.append(
        "Step 4: Set the Vertex Cover target size "
        f"k = n + 2m = {target_size}."
    )

    return ReductionResult(
        vertices=vertices,
        edges=edges,
        target_size=target_size,
        variables=variables,
        clauses=clauses,
        clause_vertices=clause_vertices,
        steps=steps,
    )


def assignment_to_vertex_cover(
    reduction: ReductionResult,
    assignment: Dict[str, bool],
) -> Set[str]:
    """
    Build a Vertex Cover from a satisfying assignment.

    One true literal vertex is selected for each variable.
    Two vertices are selected from each clause triangle,
    leaving one true clause occurrence outside the cover.
    """
    if not evaluate_formula(
        reduction.clauses,
        assignment,
    ):
        raise ValueError(
            "assignment must satisfy the formula"
        )

    cover: Set[str] = set()

    for variable in reduction.variables:
        if assignment[
            variable
        ]:
            cover.add(
                variable
            )
        else:
            cover.add(
                f"~{variable}"
            )

    for clause_index, clause in enumerate(
        reduction.clauses
    ):
        true_occurrence_index = next(
            index
            for index, literal in enumerate(
                clause
            )
            if evaluate_literal(
                literal,
                assignment,
            )
        )

        for occurrence_index, vertex in enumerate(
            reduction.clause_vertices[
                clause_index
            ]
        ):
            if (
                occurrence_index
                != true_occurrence_index
            ):
                cover.add(
                    vertex
                )

    return cover


def is_vertex_cover(
    edges: Iterable[Edge],
    cover: Set[str],
) -> bool:
    """Return True when every edge has at least one endpoint in the cover."""
    return all(
        first in cover
        or second in cover
        for first, second in edges
    )


def explain_reduction(
    reduction: ReductionResult,
) -> str:
    """Return a printable explanation of the reduction."""
    return "\n".join(
        reduction.steps
    )