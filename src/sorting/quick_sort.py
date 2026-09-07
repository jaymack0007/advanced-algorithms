"""
Randomized QuickSort implementation with small-array optimization.

This version uses:
- Randomized pivot selection
- Three-way partitioning
- Insertion sort for small subarrays
- A copied input list so the original is not modified
"""

import random
from typing import List, Tuple, TypeVar

T = TypeVar("T")

INSERTION_SORT_THRESHOLD = 10


def _insertion_sort_range(
    arr: List[T],
    low: int,
    high: int,
) -> None:
    """
    Sort part of a list in place using insertion sort.

    This helper is used for small QuickSort subarrays because
    insertion sort has less overhead on small inputs.

    Args:
        arr: List being sorted.
        low: Starting index of the section.
        high: Ending index of the section.
    """
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1

        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key


def partition(
    arr: List[T],
    low: int,
    high: int,
) -> Tuple[int, int]:
    """
    Partition a list section around a randomly selected pivot.

    Three-way partitioning separates the values into:

        values < pivot
        values == pivot
        values > pivot

    Args:
        arr: List being partitioned.
        low: Starting index.
        high: Ending index.

    Returns:
        A tuple containing the first and last index of the
        section containing values equal to the pivot.

    Time Complexity:
        O(n) for the section being partitioned.

    Space Complexity:
        O(1) auxiliary space.
    """
    pivot_index = random.randint(low, high)
    pivot = arr[pivot_index]

    less_than = low
    current = low
    greater_than = high

    while current <= greater_than:

        if arr[current] < pivot:
            arr[less_than], arr[current] = (
                arr[current],
                arr[less_than],
            )

            less_than += 1
            current += 1

        elif arr[current] > pivot:
            arr[current], arr[greater_than] = (
                arr[greater_than],
                arr[current],
            )

            greater_than -= 1

        else:
            current += 1

    return less_than, greater_than


def _quick_sort(
    arr: List[T],
    low: int,
    high: int,
) -> None:
    """
    Recursively sort a section of a list using QuickSort.
    """
    if low >= high:
        return

    # Small sections are faster with insertion sort.
    if high - low + 1 <= INSERTION_SORT_THRESHOLD:
        _insertion_sort_range(arr, low, high)
        return

    equal_start, equal_end = partition(
        arr,
        low,
        high,
    )

    _quick_sort(
        arr,
        low,
        equal_start - 1,
    )

    _quick_sort(
        arr,
        equal_end + 1,
        high,
    )


def quick_sort(arr: List[T]) -> List[T]:
    """
    Sort a list using randomized QuickSort.

    A random pivot is selected during each partition step.
    Three-way partitioning is used so duplicate values can
    be handled efficiently. Small subarrays are sorted using
    insertion sort.

    Args:
        arr: List of comparable values to sort.

    Returns:
        A new sorted list. The original input is not modified.

    Raises:
        TypeError: If arr is not a list.

    Time Complexity:
        Best Case: O(n log n)
        Average Case: O(n log n)
        Worst Case: O(n^2)

    Space Complexity:
        O(log n) expected recursion space.

    Stability:
        Not stable.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a list")

    result = arr.copy()

    if len(result) <= 1:
        return result

    _quick_sort(
        result,
        0,
        len(result) - 1,
    )

    return result