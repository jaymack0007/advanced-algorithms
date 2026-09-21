# Advanced Algorithms



Jaymes McKenzie



This repository contains coursework and benchmarking projects for CSC5300 Advanced Algorithms.



## Week 1



Implemented and compared:



* Bubble Sort
* Selection Sort
* Insertion Sort



## Week 2



Added divide-and-conquer sorting algorithms:



* Merge Sort
* QuickSort



Benchmarks compared all five sorting algorithms across multiple input sizes and data types.



## Week 3



Implemented and analyzed:



* Binary Min-Heap
* Binary Max-Heap
* Priority Queue
* AVL Tree
* Hash Table with Separate Chaining
* Hash Table with Open Addressing



Week 3 benchmarks compare custom data structures with Python `heapq`, `dict`, and list search.



## Week 4



Implemented and analyzed:



* Adjacency List Graph
* Adjacency Matrix Graph
* Breadth-First Search
* Iterative Depth-First Search
* Recursive Depth-First Search
* Dijkstra's Shortest Path Algorithm
* Heap-Based Priority Queue
* List-Based Priority Queue
* Graph Generation and Visualization



Week 4 benchmarks compare adjacency list and matrix representations, BFS and DFS on sparse and dense graphs, and heap-based versus list-based Dijkstra.



## Project Structure



```text

src/

├── sorting/

├── structures/

├── graphs/

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

.\\.venv\\Scripts\\Activate.ps1

```



Install the required packages:



```powershell

python -m pip install -r requirements.txt

```



\## Run Tests



```powershell

python -m pytest tests\\ -v

```



\## Run Week 4 Demo



```powershell

python .\\examples\\week4\_demo.py

```



\## Run Week 4 Benchmarks



```powershell

python .\\benchmarks\\week4\_graph\_benchmark.py

```



Week 4 benchmark results are stored in:



```text

benchmarks/results/

```



The Week 4 report is located at:



```text

analysis/week4\_report.md

```

