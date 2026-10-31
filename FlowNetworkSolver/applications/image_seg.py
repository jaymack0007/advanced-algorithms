"""Grayscale image segmentation using an s-t graph cut."""

from collections import deque
from dataclasses import dataclass
import math
from numbers import Real
from typing import List, Sequence, Set, Tuple

from FlowNetworkSolver.core.network import (
    FlowNetwork,
)
from FlowNetworkSolver.core.push_relabel import (
    PushRelabelResult,
    push_relabel,
)


Pixel = Tuple[int, int]


@dataclass
class SegmentationResult:
    """Store the output of grayscale graph-cut segmentation."""

    mask: List[
        List[int]
    ]
    foreground_pixels: Set[Pixel]
    background_pixels: Set[Pixel]
    cut_value: float
    max_flow_result: PushRelabelResult


def _validate_number(
    value,
    name: str,
    minimum: float = 0.0,
    maximum: float | None = None,
) -> float:
    """Validate a finite numeric parameter."""
    if (
        isinstance(
            value,
            bool,
        )
        or not isinstance(
            value,
            Real,
        )
    ):
        raise TypeError(
            f"{name} must be numeric"
        )

    result = float(
        value
    )

    if not math.isfinite(
        result
    ):
        raise ValueError(
            f"{name} must be finite"
        )

    if result < minimum:
        raise ValueError(
            f"{name} must be at least {minimum}"
        )

    if (
        maximum is not None
        and result > maximum
    ):
        raise ValueError(
            f"{name} must be at most {maximum}"
        )

    return result


def _validate_image(
    image: Sequence[
        Sequence[float]
    ],
) -> List[
    List[float]
]:
    """Validate and normalize a rectangular grayscale image."""
    if not isinstance(
        image,
        (list, tuple),
    ):
        raise TypeError(
            "image must be a list or tuple of rows"
        )

    if not image:
        raise ValueError(
            "image must not be empty"
        )

    first_row = image[
        0
    ]

    if not isinstance(
        first_row,
        (list, tuple),
    ):
        raise TypeError(
            "image rows must be lists or tuples"
        )

    if not first_row:
        raise ValueError(
            "image rows must not be empty"
        )

    width = len(
        first_row
    )

    normalized = []

    for row in image:
        if not isinstance(
            row,
            (list, tuple),
        ):
            raise TypeError(
                "image rows must be lists or tuples"
            )

        if len(
            row
        ) != width:
            raise ValueError(
                "image must be rectangular"
            )

        normalized_row = []

        for value in row:
            normalized_row.append(
                _validate_number(
                    value,
                    "pixel intensity",
                    minimum=0.0,
                    maximum=255.0,
                )
            )

        normalized.append(
            normalized_row
        )

    return normalized


def build_segmentation_network(
    image: Sequence[
        Sequence[float]
    ],
    foreground_reference: float = 220.0,
    background_reference: float = 30.0,
    data_weight: float = 1.0,
    smoothness: float = 10.0,
) -> Tuple[
    FlowNetwork,
    str,
    str,
    List[
        List[float]
    ],
]:
    """
    Build an s-t graph for grayscale image segmentation.

    Terminal edges encode foreground/background likelihood.
    Neighbor edges penalize separating visually similar pixels.
    """
    pixels = _validate_image(
        image
    )

    foreground_value = _validate_number(
        foreground_reference,
        "foreground_reference",
        minimum=0.0,
        maximum=255.0,
    )

    background_value = _validate_number(
        background_reference,
        "background_reference",
        minimum=0.0,
        maximum=255.0,
    )

    data_scale = _validate_number(
        data_weight,
        "data_weight",
    )

    smoothness_scale = _validate_number(
        smoothness,
        "smoothness",
    )

    source = "__foreground__"
    sink = "__background__"

    network = FlowNetwork()

    network.add_node(
        source
    )

    network.add_node(
        sink
    )

    height = len(
        pixels
    )

    width = len(
        pixels[
            0
        ]
    )

    for row in range(
        height
    ):
        for column in range(
            width
        ):
            pixel = (
                row,
                column,
            )

            intensity = pixels[
                row
            ][
                column
            ]

            background_cost = (
                data_scale
                * abs(
                    intensity
                    - background_value
                )
            )

            foreground_cost = (
                data_scale
                * abs(
                    intensity
                    - foreground_value
                )
            )

            # If the pixel is placed on the background side,
            # source -> pixel is cut.
            network.add_edge(
                source,
                pixel,
                background_cost,
            )

            # If the pixel is placed on the foreground side,
            # pixel -> sink is cut.
            network.add_edge(
                pixel,
                sink,
                foreground_cost,
            )

    for row in range(
        height
    ):
        for column in range(
            width
        ):
            current = (
                row,
                column,
            )

            neighbors = []

            if column + 1 < width:
                neighbors.append(
                    (
                        row,
                        column + 1,
                    )
                )

            if row + 1 < height:
                neighbors.append(
                    (
                        row + 1,
                        column,
                    )
                )

            for neighbor in neighbors:
                neighbor_row, neighbor_column = (
                    neighbor
                )

                difference = abs(
                    pixels[
                        row
                    ][
                        column
                    ]
                    - pixels[
                        neighbor_row
                    ][
                        neighbor_column
                    ]
                )

                similarity = (
                    smoothness_scale
                    / (
                        1.0
                        + difference
                    )
                )

                # Two directed edges model one undirected
                # smoothness penalty in the s-t cut.
                network.add_edge(
                    current,
                    neighbor,
                    similarity,
                )

                network.add_edge(
                    neighbor,
                    current,
                    similarity,
                )

    return (
        network,
        source,
        sink,
        pixels,
    )


def _source_side_of_cut(
    network: FlowNetwork,
    source: str,
    tolerance: float = 1e-12,
) -> set:
    """Return vertices reachable from source in the residual graph."""
    reachable = {
        source
    }

    queue = deque(
        [
            source
        ]
    )

    while queue:
        current = queue.popleft()

        for edge in network.adjacency[
            current
        ]:
            if (
                edge.residual_capacity
                <= tolerance
            ):
                continue

            if edge.to in reachable:
                continue

            reachable.add(
                edge.to
            )

            queue.append(
                edge.to
            )

    return reachable


def segment_grayscale(
    image: Sequence[
        Sequence[float]
    ],
    foreground_reference: float = 220.0,
    background_reference: float = 30.0,
    data_weight: float = 1.0,
    smoothness: float = 10.0,
) -> SegmentationResult:
    """
    Segment a grayscale image into foreground and background.

    Mask values:
        1 = foreground
        0 = background
    """
    (
        network,
        source,
        sink,
        pixels,
    ) = build_segmentation_network(
        image,
        foreground_reference=foreground_reference,
        background_reference=background_reference,
        data_weight=data_weight,
        smoothness=smoothness,
    )

    flow_result = push_relabel(
        network,
        source,
        sink,
    )

    source_side = _source_side_of_cut(
        network,
        source,
    )

    foreground_pixels: Set[
        Pixel
    ] = set()

    background_pixels: Set[
        Pixel
    ] = set()

    mask = []

    for row in range(
        len(
            pixels
        )
    ):
        mask_row = []

        for column in range(
            len(
                pixels[
                    row
                ]
            )
        ):
            pixel = (
                row,
                column,
            )

            if pixel in source_side:
                foreground_pixels.add(
                    pixel
                )

                mask_row.append(
                    1
                )
            else:
                background_pixels.add(
                    pixel
                )

                mask_row.append(
                    0
                )

        mask.append(
            mask_row
        )

    return SegmentationResult(
        mask=mask,
        foreground_pixels=foreground_pixels,
        background_pixels=background_pixels,
        cut_value=flow_result.max_flow,
        max_flow_result=flow_result,
    )