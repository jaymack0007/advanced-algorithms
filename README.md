# Advanced Algorithms



Jaymes McKenzie



This repository contains coursework and benchmarking projects for CSC5300 Advanced Algorithms.



## Week 1



Implemented and compared:



- Bubble Sort

- Selection Sort

- Insertion Sort



Benchmarks compared the sorting algorithms across different input sizes and data types.



## Week 2



Added divide-and-conquer sorting algorithms:



- Merge Sort

- QuickSort



Benchmarks compared all five sorting algorithms across random, sorted, reverse, nearly sorted, and duplicate-heavy data.



## Week 3



Implemented and analyzed:



- Binary Min-Heap

- Binary Max-Heap

- Priority Queue

- AVL Tree

- Hash Table with Separate Chaining

- Hash Table with Open Addressing



Week 3 benchmarks compared custom data structures with Python `heapq`, `dict`, and list search.



## Week 4



Implemented and analyzed:



- Adjacency List Graph

- Adjacency Matrix Graph

- Breadth-First Search

- Iterative Depth-First Search

- Recursive Depth-First Search

- Dijkstra's Shortest Path Algorithm

- Heap-Based Priority Queue

- List-Based Priority Queue

- Graph Generation and Visualization



Week 4 benchmarks compared adjacency list and matrix representations, BFS and DFS on sparse and dense graphs, and heap-based versus list-based Dijkstra.



## Week 5



Implemented and analyzed dynamic programming solutions for:



- Fibonacci

- 0/1 Knapsack

- Longest Common Subsequence



Each problem includes recursive and dynamic programming approaches.



Fibonacci includes:



- Naive Recursion

- Top-Down Memoization

- Bottom-Up Tabulation



Knapsack includes:



- Naive Recursion

- Top-Down Memoization

- Bottom-Up Tabulation

- Optimal item reconstruction



Longest Common Subsequence includes:



- Naive Recursion

- Top-Down Memoization

- Bottom-Up Tabulation

- Subsequence reconstruction



Week 5 benchmarks compare execution time, memory use, recursive calls, recursion depth, and available speedup values. Larger naive recursive inputs are skipped when exponential growth makes direct execution impractical.



## Project Structure



```text

src/

├── sorting/

├── structures/

├── graphs/

├── dp/

└── utils/



tests/

benchmarks/

analysis/

examples/

```



## Setup



This project was developed using Python 3.14.5.



Create and activate a virtual environment:



```powershell

py -3.14 -m venv .venv

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\.venv\Scripts\Activate.ps1

```



Install the required packages:



```powershell

python -m pip install -r requirements.txt

```



## Run All Tests



```powershell

python -m pytest .\tests\ -q

```



## Week 5 Tests



Run individual Week 5 test files:



```powershell

python -m pytest .\tests\test_fibonacci.py -v

python -m pytest .\tests\test_knapsack.py -v

python -m pytest .\tests\test_lcs.py -v

python -m pytest .\tests\test_dp_benchmark.py -v

```



## Run Week 5 Demo



```powershell

python .\examples\week5_demo.py

```



## Run Week 5 Benchmarks



```powershell

python .\benchmarks\week5_dp_benchmark.py

```



Week 5 benchmark results are stored in:



```text

benchmarks/results/

```



Required Week 5 result files:



```text

fibonacci_comparison.png

knapsack_performance.png

lcs_performance.png

dp_vs_recursive_table.csv

```



The Week 5 technical report is located at:



```text

analysis/week5_report.md

```

