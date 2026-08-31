"""
Basic sorting algorithms implementation with comprehensive documentation.
"""

from typing import List, TypeVar

T = TypeVar("T")


def bubble_sort(arr: List[T]) -> List[T]:
    """
    Sort an array using the bubble sort algorithm.

    Bubble sort repeatedly steps through the list, compares adjacent elements,
    and swaps them if they are in the wrong order.

    Args:
        arr: List of comparable elements to sort.

    Returns:
        New sorted list. The original list is not modified.

    Time Complexity:
        Best Case: O(n) when array is already sorted
        Average Case: O(n^2)
        Worst Case: O(n^2)

    Space Complexity:
        O(1) auxiliary space for the sorting process.

    Stability:
        Stable
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a list")

    if len(arr) <= 1:
        return arr.copy()

    # Work on a copy so the original list is not changed.
    result = arr.copy()
    n = len(result)

    for i in range(n):
        swapped = False

        # Last i elements are already in their correct positions.
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        # Optimization: stop early if no swaps occurred.
        if not swapped:
            break

    return result


def selection_sort(arr: List[T]) -> List[T]:
    """
    Sort an array using the selection sort algorithm.

    Selection sort repeatedly finds the minimum element from the unsorted
    portion of the list and places it at the beginning of that portion.

    Args:
        arr: List of comparable elements to sort.

    Returns:
        New sorted list. The original list is not modified.

    Time Complexity:
        Best Case: O(n^2)
        Average Case: O(n^2)
        Worst Case: O(n^2)

    Space Complexity:
        O(1) auxiliary space for the sorting process.

    Stability:
        Unstable
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a list")

    if len(arr) <= 1:
        return arr.copy()

    # Work on a copy so the original list is not changed.
    result = arr.copy()
    n = len(result)

    for i in range(n):
        min_idx = i

        for j in range(i + 1, n):
            if result[j] < result[min_idx]:
                min_idx = j

        result[i], result[min_idx] = result[min_idx], result[i]

    return result


def insertion_sort(arr: List[T]) -> List[T]:
    """
    Sort an array using the insertion sort algorithm.

    Insertion sort builds the sorted list one element at a time by inserting
    each new element into its proper position.

    Args:
        arr: List of comparable elements to sort.

    Returns:
        New sorted list. The original list is not modified.

    Time Complexity:
        Best Case: O(n) when array is already sorted
        Average Case: O(n^2)
        Worst Case: O(n^2)

    Space Complexity:
        O(1) auxiliary space for the sorting process.

    Stability:
        Stable

    Adaptive:
        Yes, especially useful for nearly sorted data.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a list")

    if len(arr) <= 1:
        return arr.copy()

    # Work on a copy so the original list is not changed.
    result = arr.copy()

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = key

    return result


def analyze_array_characteristics(arr: List[T]) -> dict:
    """
    Analyze characteristics of an array to help choose an algorithm.

    Args:
        arr: List to analyze.

    Returns:
        Dictionary containing information about the array.
    """
    if not arr:
        return {
            "size": 0,
            "inversions": 0,
            "sorted_percentage": 100
        }

    n = len(arr)

    inversions = sum(
        1 for i in range(n - 1)
        if arr[i] > arr[i + 1]
    )

    sorted_percentage = (
        ((n - 1) - inversions) / (n - 1) * 100
        if n > 1
        else 100
    )

    return {
        "size": n,
        "inversions": inversions,
        "sorted_percentage": round(sorted_percentage, 2),
        "recommended_algorithm": _recommend_algorithm(
            n,
            sorted_percentage
        )
    }


def _recommend_algorithm(size: int, sorted_percentage: float) -> str:
    """
    Recommend a sorting algorithm based on array characteristics.
    """
    if size <= 20:
        return "insertion_sort (small array)"
    elif sorted_percentage >= 90:
        return "insertion_sort (nearly sorted)"
    elif size <= 1000:
        return "selection_sort (medium array)"
    else:
        return "advanced_sort (large array - implement merge/quick sort)"