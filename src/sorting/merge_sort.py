"""
Merge sort implementation using the divide-and-conquer approach.
"""

from typing import List, TypeVar

T = TypeVar("T")


def merge(left: List[T], right: List[T]) -> List[T]:
    """
    Merge two sorted lists into one sorted list.

    Args:
        left: First sorted list.
        right: Second sorted list.

    Returns:
        A new list containing all values from left and right in sorted order.

    Time Complexity:
        O(n + m), where n and m are the lengths of the two input lists.

    Space Complexity:
        O(n + m)
    """
    merged = []

    left_index = 0
    right_index = 0

    while (
        left_index < len(left)
        and right_index < len(right)
    ):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    # Add any values that remain in either list.
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])

    return merged


def merge_sort(arr: List[T]) -> List[T]:
    """
    Sort a list using the merge sort algorithm.

    Merge sort follows the divide-and-conquer pattern:

    1. Divide the list into two halves.
    2. Recursively sort each half.
    3. Merge the two sorted halves.

    Args:
        arr: List of comparable values to sort.

    Returns:
        A new sorted list. The original list is not modified.

    Raises:
        TypeError: If arr is not a list.

    Time Complexity:
        Best Case: O(n log n)
        Average Case: O(n log n)
        Worst Case: O(n log n)

    Space Complexity:
        O(n)

    Stability:
        Stable
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a list")

    # Base case.
    if len(arr) <= 1:
        return arr.copy()

    # Divide.
    middle = len(arr) // 2

    left_half = arr[:middle]
    right_half = arr[middle:]

    # Conquer.
    sorted_left = merge_sort(left_half)
    sorted_right = merge_sort(right_half)

    # Combine.
    return merge(sorted_left, sorted_right)