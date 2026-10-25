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



## Week 6

Implemented and analyzed advanced dynamic programming techniques:

- Space-Optimized 0/1 Knapsack
- Matrix Chain Multiplication
- Floyd-Warshall All-Pairs Shortest Paths
- Bitmask Dynamic Programming for Traveling Salesman

Week 6 focuses on reducing memory use, representing DP states efficiently, solving interval-based problems, and applying dynamic programming to graphs.

The benchmarks compare:

- Standard vs space-optimized Knapsack
- Memoized vs bottom-up Matrix Chain Multiplication
- Floyd-Warshall scaling and repeated Dijkstra comparison
- Bitmask TSP vs brute force

Results include runtime, memory usage, speedup measurements, plots, and a CSV comparison table.

## Week 7

Implemented and analyzed randomized and probabilistic algorithms:

- Randomized QuickSort
- Randomized QuickSelect
- Fermat Primality Testing
- Miller-Rabin Primality Testing
- Bloom Filter Membership Testing
- MinHash Similarity Estimation

Week 7 focuses on using randomness to improve expected performance, avoid poor input patterns, and trade small amounts of uncertainty for speed or memory efficiency.

The benchmarks compare:

- Randomized vs deterministic QuickSort
- Randomized vs deterministic selection
- Fermat and Miller-Rabin primality testing
- Bloom filter observed vs theoretical false-positive rates
- MinHash estimates vs exact Jaccard similarity

Results include runtime, runtime variance, comparison counts, recursion depth, accuracy, error rates, probabilistic bounds, plots, and a summary CSV.

## Week 8

Implemented and analyzed computational complexity, NP-completeness, and approximation techniques:

- 3-SAT to Vertex Cover polynomial-time reduction
- Exact backtracking for Subset Sum
- Greedy Subset Sum heuristic
- Exact DFS/backtracking SAT solver
- Randomized SAT heuristic
- Exact exhaustive Vertex Cover
- Vertex Cover 2-approximation
- Exact exhaustive Traveling Salesman Problem
- Nearest Neighbor TSP heuristic

Week 8 focuses on exponential and factorial growth, polynomial-time reductions, and the trade-off between exact solutions and faster approximation or heuristic methods.

The benchmarks compare exact and practical methods for Subset Sum, SAT, Vertex Cover, and TSP. Results include runtime growth, search-node counts, heuristic success rates, approximation ratios, runtime-quality trade-offs, plots, and a comparison CSV.

Week 8 demo: examples/week8_demo.py

Week 8 benchmark: benchmarks/week8_complexity_benchmark.py

Required results: runtime_growth.png, approximation_quality.png, and comparison_table.csv.

Technical report: analysis/week8_report.md

## Week 9

Implemented and analyzed approximation, LP-rounding, greedy, and randomized algorithms:

- Vertex Cover maximal-matching 2-approximation
- Greedy Uncapacitated Facility Location
- Set Cover LP relaxation
- Deterministic Set Cover LP rounding
- Randomized Set Cover LP rounding
- Metric TSP MST-doubling 2-approximation
- Randomized Max-Cut
- Local-search Max-Cut

Week 9 focuses on designing efficient solutions when exact optimization is impractical. Exact exhaustive algorithms are used on small instances as baselines so approximation quality can be measured directly.

The benchmarks compare:

- Vertex Cover 2-approximation vs exact Vertex Cover
- Greedy Facility Location vs exact Facility Location
- Deterministic and randomized Set Cover LP rounding vs exact Set Cover
- Metric TSP MST doubling vs exact TSP
- Randomized and local-search Max-Cut vs exact Max-Cut

Measured results include runtime, approximation ratios, optimal costs or values, LP lower bounds, randomized solution variance, and runtime variance.

Week 9 demo: examples/week9_demo.py

Week 9 benchmark: benchmarks/week9_approx_benchmark.py

Required results: approx_ratios.png, cost_vs_optimal.png, randomized_maxcut_results.png, and comparison_table.csv.

Technical report: analysis/week9_report.md

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

