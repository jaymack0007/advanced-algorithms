"""Simple Week 2 demonstration of Merge Sort and QuickSort."""

import sys
from pathlib import Path


# Add the project root so src can be imported when this
# file is run directly from the examples folder.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.sorting import merge_sort, quick_sort


def main():
    data = [38, 27, 43, 3, 9, 82, 10]

    print("Original data:")
    print(data)

    print("\nMerge Sort:")
    print(merge_sort(data))

    print("\nQuickSort:")
    print(quick_sort(data))

    print("\nOriginal data after sorting:")
    print(data)


if __name__ == "__main__":
    main()