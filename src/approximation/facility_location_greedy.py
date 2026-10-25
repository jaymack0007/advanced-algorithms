"""Greedy heuristic and exact baseline for Facility Location."""

from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, List, Mapping, Set, Tuple


ServiceCosts = Mapping[Tuple[str, str], float]


@dataclass
class FacilityLocationResult:
    """Store a facility-location solution."""

    open_facilities: Set[str]
    assignments: Dict[str, str]
    total_cost: float
    opening_cost: float
    service_cost: float


def _validate_inputs(
    opening_costs: Mapping[str, float],
    clients: Iterable[str],
    service_costs: ServiceCosts,
) -> List[str]:
    """Validate a facility-location instance."""
    if not isinstance(
        opening_costs,
        dict,
    ):
        raise TypeError(
            "opening_costs must be a dictionary"
        )

    if not isinstance(
        clients,
        (list, tuple),
    ):
        raise TypeError(
            "clients must be a list or tuple"
        )

    if not isinstance(
        service_costs,
        dict,
    ):
        raise TypeError(
            "service_costs must be a dictionary"
        )

    client_list = list(
        clients
    )

    if len(
        client_list
    ) != len(
        set(client_list)
    ):
        raise ValueError(
            "clients must be unique"
        )

    for client in client_list:
        if not isinstance(
            client,
            str,
        ):
            raise TypeError(
                "client names must be strings"
            )

    for facility, cost in opening_costs.items():
        if not isinstance(
            facility,
            str,
        ):
            raise TypeError(
                "facility names must be strings"
            )

        if not isinstance(
            cost,
            (int, float),
        ):
            raise TypeError(
                "opening costs must be numeric"
            )

        if cost < 0:
            raise ValueError(
                "opening costs must be non-negative"
            )

    if client_list and not opening_costs:
        raise ValueError(
            "at least one facility is required when clients exist"
        )

    for facility in opening_costs:
        for client in client_list:
            key = (
                facility,
                client,
            )

            if key not in service_costs:
                raise ValueError(
                    f"missing service cost for {facility}, {client}"
                )

            cost = service_costs[
                key
            ]

            if not isinstance(
                cost,
                (int, float),
            ):
                raise TypeError(
                    "service costs must be numeric"
                )

            if cost < 0:
                raise ValueError(
                    "service costs must be non-negative"
                )

    return client_list


def evaluate_solution(
    opening_costs: Mapping[str, float],
    clients: Iterable[str],
    service_costs: ServiceCosts,
    open_facilities: Set[str],
) -> FacilityLocationResult:
    """
    Assign each client to its cheapest open facility.

    Ties are broken by facility name for reproducibility.
    """
    client_list = _validate_inputs(
        opening_costs,
        clients,
        service_costs,
    )

    if not isinstance(
        open_facilities,
        set,
    ):
        raise TypeError(
            "open_facilities must be a set"
        )

    unknown = (
        open_facilities
        - set(
            opening_costs
        )
    )

    if unknown:
        raise ValueError(
            "open_facilities contains an unknown facility"
        )

    if client_list and not open_facilities:
        raise ValueError(
            "at least one facility must be open"
        )

    assignments: Dict[
        str,
        str,
    ] = {}

    opening_total = sum(
        opening_costs[
            facility
        ]
        for facility in open_facilities
    )

    service_total = 0.0

    for client in client_list:
        facility = min(
            open_facilities,
            key=lambda name: (
                service_costs[
                    (
                        name,
                        client,
                    )
                ],
                name,
            ),
        )

        assignments[
            client
        ] = facility

        service_total += service_costs[
            (
                facility,
                client,
            )
        ]

    return FacilityLocationResult(
        open_facilities=set(
            open_facilities
        ),
        assignments=assignments,
        total_cost=(
            float(
                opening_total
            )
            + float(
                service_total
            )
        ),
        opening_cost=float(
            opening_total
        ),
        service_cost=float(
            service_total
        ),
    )


def greedy_facility_location(
    opening_costs: Mapping[str, float],
    clients: Iterable[str],
    service_costs: ServiceCosts,
) -> FacilityLocationResult:
    """
    Solve Facility Location with an add-only greedy heuristic.

    The algorithm first selects the best single facility.
    It then repeatedly opens the facility that produces
    the greatest decrease in total solution cost. It stops
    when no additional facility improves the solution.
    """
    client_list = _validate_inputs(
        opening_costs,
        clients,
        service_costs,
    )

    if not client_list:
        return FacilityLocationResult(
            open_facilities=set(),
            assignments={},
            total_cost=0.0,
            opening_cost=0.0,
            service_cost=0.0,
        )

    facilities = sorted(
        opening_costs
    )

    best_result = min(
        (
            evaluate_solution(
                opening_costs,
                client_list,
                service_costs,
                {
                    facility
                },
            )
            for facility in facilities
        ),
        key=lambda result: (
            result.total_cost,
            sorted(
                result.open_facilities
            ),
        ),
    )

    while True:
        candidate_results = []

        for facility in facilities:
            if facility in best_result.open_facilities:
                continue

            candidate_open = (
                best_result.open_facilities
                | {
                    facility
                }
            )

            candidate_results.append(
                evaluate_solution(
                    opening_costs,
                    client_list,
                    service_costs,
                    candidate_open,
                )
            )

        if not candidate_results:
            break

        candidate = min(
            candidate_results,
            key=lambda result: (
                result.total_cost,
                sorted(
                    result.open_facilities
                ),
            ),
        )

        if candidate.total_cost >= best_result.total_cost:
            break

        best_result = candidate

    return best_result


def exact_facility_location(
    opening_costs: Mapping[str, float],
    clients: Iterable[str],
    service_costs: ServiceCosts,
) -> FacilityLocationResult:
    """
    Find an optimal Facility Location solution by exhaustive search.

    Intended only for small instances because all non-empty
    subsets of facilities may need to be evaluated.
    """
    client_list = _validate_inputs(
        opening_costs,
        clients,
        service_costs,
    )

    if not client_list:
        return FacilityLocationResult(
            open_facilities=set(),
            assignments={},
            total_cost=0.0,
            opening_cost=0.0,
            service_cost=0.0,
        )

    facilities = sorted(
        opening_costs
    )

    best_result = None

    for size in range(
        1,
        len(facilities) + 1,
    ):
        for subset in combinations(
            facilities,
            size,
        ):
            result = evaluate_solution(
                opening_costs,
                client_list,
                service_costs,
                set(
                    subset
                ),
            )

            if (
                best_result is None
                or result.total_cost
                < best_result.total_cost
            ):
                best_result = result

    if best_result is None:
        raise RuntimeError(
            "no facility-location solution found"
        )

    return best_result


def approximation_ratio(
    heuristic_cost: float,
    optimal_cost: float,
) -> float:
    """Return heuristic solution cost divided by optimal cost."""
    if heuristic_cost < 0:
        raise ValueError(
            "heuristic cost must be non-negative"
        )

    if optimal_cost < 0:
        raise ValueError(
            "optimal cost must be non-negative"
        )

    if optimal_cost == 0:
        if heuristic_cost == 0:
            return 1.0

        raise ValueError(
            "optimal cost cannot be zero when heuristic cost is positive"
        )

    return (
        heuristic_cost
        / optimal_cost
    )