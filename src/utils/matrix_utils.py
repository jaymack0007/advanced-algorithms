"""Utility functions for Week 6 matrix benchmarks."""

import random
from math import inf
from typing import List


def generate_weighted_graph_matrix(
    size: int,
    density: float = 0.25,
    seed: int = 42,
) -> List[List[float]]:
    """
    Generate a directed weighted graph matrix.

    Missing edges are represented by math.inf.
    All generated edge weights are positive.
    """
    if size <= 0:
        raise ValueError(
            "size must be positive"
        )

    if not 0 <= density <= 1:
        raise ValueError(
            "density must be between 0 and 1"
        )

    random_generator = random.Random(seed)

    matrix = [
        [inf] * size
        for _ in range(size)
    ]

    for vertex in range(size):
        matrix[vertex][vertex] = 0

    for i in range(size):
        for j in range(size):
            if i == j:
                continue

            if random_generator.random() < density:
                matrix[i][j] = (
                    random_generator.randint(
                        1,
                        20,
                    )
                )

    return matrix


def generate_complete_distance_matrix(
    size: int,
    seed: int = 42,
) -> List[List[float]]:
    """
    Generate a complete symmetric distance matrix.

    Used for Traveling Salesman benchmarks.
    """
    if size <= 0:
        raise ValueError(
            "size must be positive"
        )

    random_generator = random.Random(seed)

    matrix = [
        [0.0] * size
        for _ in range(size)
    ]

    for i in range(size):
        for j in range(i + 1, size):
            distance = random_generator.randint(
                1,
                100,
            )

            matrix[i][j] = distance
            matrix[j][i] = distance

    return matrix


def generate_matrix_dimensions(
    matrix_count: int,
    seed: int = 42,
) -> List[int]:
    """
    Generate dimensions for Matrix Chain Multiplication.
    """
    if matrix_count <= 0:
        raise ValueError(
            "matrix_count must be positive"
        )

    random_generator = random.Random(seed)

    return [
        random_generator.randint(
            5,
            50,
        )
        for _ in range(matrix_count + 1)
    ]