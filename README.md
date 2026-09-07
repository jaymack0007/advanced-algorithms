Advanced Algorithms Course - Week 2 Algorithm Laboratory

Jaymes McKenzie



## Description

This project builds on the Week 1 sorting project and adds Merge Sort and

QuickSort. The purpose of Week 2 is to compare the O(n²) sorting algorithms

from Week 1 with O(n log n) divide-and-conquer algorithms.



The project includes:



\- Bubble Sort

\- Selection Sort

\- Insertion Sort

\- Merge Sort

\- QuickSort



Merge Sort uses recursive divide and conquer with a merge helper function.



QuickSort includes:



\- Random pivot selection

\- Three-way partitioning

\- Insertion Sort for small subarrays

\- A threshold of 10 elements



\## Project Structure



```text

week2\_project/

├── README.md

├── src/

│   └── sorting/

│       ├── basic\_sorts.py

│       ├── merge\_sort.py

│       ├── quick\_sort.py

│       └── \_\_init\_\_.py

├── tests/

│   ├── test\_sorting.py

│   ├── test\_merge\_sort.py

│   ├── test\_quick\_sort.py

│   ├── test\_sorting\_comparison.py

│   └── test\_benchmark.py

├── benchmarks/

│   ├── week2\_performance.py

│   └── results/

├── analysis/

│   ├── week2\_report.md

│   └── master\_theorem\_exercises.md

└── examples/

&#x20;   └── week2\_demo.py

