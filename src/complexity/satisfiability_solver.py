"""Small CNF SAT solvers using backtracking and random search."""

import random
from typing import Dict, List, Optional, Tuple


Literal = str
Clause = Tuple[Literal, ...]
CNF = List[Clause]


def literal_variable(
    literal: Literal,
) -> str:
    """Return the variable name from a literal."""
    if literal.startswith("~"):
        return literal[1:]

    return literal


def evaluate_literal(
    literal: Literal,
    assignment: Dict[str, bool],
) -> bool:
    """Evaluate one literal under a complete assignment."""
    variable = literal_variable(
        literal
    )

    if variable not in assignment:
        raise KeyError(
            f"missing assignment for {variable}"
        )

    value = assignment[
        variable
    ]

    if literal.startswith("~"):
        return not value

    return value


def evaluate_formula(
    clauses: CNF,
    assignment: Dict[str, bool],
) -> bool:
    """Return True when every CNF clause is satisfied."""
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


def _validate_formula(
    clauses: CNF,
) -> None:
    """Validate the CNF representation."""
    if not isinstance(
        clauses,
        list,
    ):
        raise TypeError(
            "clauses must be a list"
        )

    for clause in clauses:
        if not isinstance(
            clause,
            tuple,
        ):
            raise TypeError(
                "each clause must be a tuple"
            )

        if len(clause) == 0:
            raise ValueError(
                "clauses must not be empty"
            )

        for literal in clause:
            if not isinstance(
                literal,
                str,
            ):
                raise TypeError(
                    "literals must be strings"
                )

            variable = literal_variable(
                literal
            )

            if not variable:
                raise ValueError(
                    "literal must contain a variable name"
                )


def _clause_status(
    clause: Clause,
    assignment: Dict[str, bool],
) -> Optional[bool]:
    """
    Evaluate a clause under a partial assignment.

    Returns:
        True if already satisfied.
        False if all literals are assigned and false.
        None if the clause is still undecided.
    """
    undecided = False

    for literal in clause:
        variable = literal_variable(
            literal
        )

        if variable not in assignment:
            undecided = True
            continue

        if evaluate_literal(
            literal,
            assignment,
        ):
            return True

    if undecided:
        return None

    return False


def _formula_has_conflict(
    clauses: CNF,
    assignment: Dict[str, bool],
) -> bool:
    """Return True if a partial assignment falsifies any clause."""
    return any(
        _clause_status(
            clause,
            assignment,
        ) is False
        for clause in clauses
    )


def sat_backtracking(
    clauses: CNF,
    stats: Optional[
        Dict[str, int]
    ] = None,
) -> Optional[Dict[str, bool]]:
    """
    Solve a CNF formula using DFS/backtracking.

    Worst-case complexity is exponential in the number
    of Boolean variables.
    """
    _validate_formula(
        clauses
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

    if stats is not None:
        stats.clear()
        stats["nodes_visited"] = 0
        stats["max_depth"] = 0

    def search(
        index: int,
        assignment: Dict[str, bool],
    ) -> Optional[Dict[str, bool]]:
        if stats is not None:
            stats["nodes_visited"] += 1
            stats["max_depth"] = max(
                stats["max_depth"],
                index,
            )

        if _formula_has_conflict(
            clauses,
            assignment,
        ):
            return None

        if index == len(
            variables
        ):
            if evaluate_formula(
                clauses,
                assignment,
            ):
                return assignment.copy()

            return None

        variable = variables[
            index
        ]

        for value in (
            True,
            False,
        ):
            assignment[
                variable
            ] = value

            result = search(
                index + 1,
                assignment,
            )

            if result is not None:
                return result

        assignment.pop(
            variable,
            None,
        )

        return None

    return search(
        0,
        {},
    )


def random_sat_heuristic(
    clauses: CNF,
    trials: int = 100,
    seed: Optional[int] = None,
) -> Optional[Dict[str, bool]]:
    """
    Try random Boolean assignments.

    This heuristic is fast for small trial counts but
    is not guaranteed to find an existing solution.
    """
    _validate_formula(
        clauses
    )

    if not isinstance(
        trials,
        int,
    ):
        raise TypeError(
            "trials must be an integer"
        )

    if trials <= 0:
        raise ValueError(
            "trials must be positive"
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

    random_generator = random.Random(
        seed
    )

    for _ in range(
        trials
    ):
        assignment = {
            variable: random_generator.choice(
                [
                    False,
                    True,
                ]
            )
            for variable in variables
        }

        if evaluate_formula(
            clauses,
            assignment,
        ):
            return assignment

    return None