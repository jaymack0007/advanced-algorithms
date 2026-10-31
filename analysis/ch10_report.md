\# Week 10 Report: Advanced Graph Algorithms and Flow Networks



\## Executive Summary



This project implemented a modular Flow Network Solver containing three major algorithms: Edmonds–Karp, Push–Relabel, and Min-Cost Max-Flow. The project also applied flow-network ideas to bipartite matching, grayscale image segmentation, and scheduling/resource allocation. Supporting modules were added for graph generation, flow validation, static visualization, algorithm animation, and command-line execution.



The final benchmark tested both sparse and denser graphs. The sparse scaling experiment increased from 1,000 to 50,000 vertices. All three algorithms returned the same maximum-flow value at every tested size, which confirmed that the implementations were solving equivalent flow problems. On the sparse chain topology, Edmonds–Karp was the fastest algorithm, completing the 50,000-vertex case in 0.923425 seconds. Push–Relabel required 1.750802 seconds, while Min-Cost Max-Flow required 1.425586 seconds. Peak traced memory at 50,000 vertices ranged from 45.115 MB to 51.126 MB.



The results show that algorithm performance depends strongly on graph structure. Push–Relabel is designed for strong general max-flow performance, but the sparse chain gave Edmonds–Karp a very favorable case because there was essentially one direct augmenting route through the network. Min-Cost Max-Flow added the overhead of shortest-path and cost calculations, which became especially visible on denser graphs.



\## Implementation



The core network representation uses adjacency lists and explicit residual edges. Every original edge stores its capacity, cost, flow, reverse-edge index, and residual status. When flow is augmented on an edge, the matching reverse edge is updated at the same time. This makes cancellation and rerouting of flow possible without rebuilding the graph.



Edmonds–Karp was implemented using breadth-first search to find the shortest augmenting path in terms of edge count. After each BFS, the algorithm finds the path bottleneck, augments that amount of flow, and repeats until no source-to-sink path remains in the residual graph. The implementation records augmenting paths, bottlenecks, iteration count, and residual updates. Its standard theoretical time complexity is O(VE²).



Push–Relabel uses a preflow approach instead of repeatedly searching for complete source-to-sink paths. The source begins with a height equal to the number of vertices and saturates its outgoing edges. Active vertices then push excess flow along admissible residual edges. If no admissible edge exists, the vertex is relabeled. The implementation uses a FIFO active queue and current-edge pointers. Event history is optional so large benchmarks do not consume unnecessary memory.



Min-Cost Max-Flow uses successive shortest augmenting paths with Johnson-style vertex potentials. Bellman–Ford is used initially so negative edge costs can be supported and reachable negative-cost cycles can be detected. Later augmentations use Dijkstra’s algorithm with reduced costs. The solver returns both maximum flow and minimum total cost, along with path costs, bottlenecks, augmentation count, and final potentials.



\## Applications



Three applications were built on top of the flow algorithms. Bipartite matching converts left-side and right-side vertices into a unit-capacity network. The source connects to left vertices, valid matching edges connect left to right, and right vertices connect to the sink. A flow of one across a left-to-right edge represents one match.



The image-segmentation module models each grayscale pixel as a graph vertex. Source and sink capacities represent foreground and background costs, while neighboring pixels receive similarity edges. Push–Relabel computes the s–t cut, and pixels reachable from the source in the final residual graph are labeled foreground. The result is returned as a binary mask.



The scheduling application models jobs and machines as a capacity-constrained flow problem. Each job has source capacity one, eligible job-to-machine assignments have capacity one, and each machine-to-sink edge uses that machine’s available capacity. The resulting maximum flow gives the largest feasible set of assignments and identifies any jobs that could not be scheduled.



\## Validation, Visualization, and Interface



Reusable validators check edge capacities, flow conservation, source/sink balance, residual-edge consistency, and Min-Cost Flow feasibility. Reproducible generators create sparse networks, dense directed acyclic networks, bipartite graphs, grids, and capacity distributions.



The visualization layer produces static network diagrams with flow/capacity labels. Edmonds–Karp animations highlight augmenting paths and bottleneck values. Push–Relabel animations display recorded push and relabel events. A command-line interface supports all three solvers plus matching, segmentation, and scheduling using JSON input files.



The complete automated test suite reached 677 passing tests before the final benchmark. Additional benchmark-specific tests verified network generation, solver measurement, and agreement among the three algorithms.



\## Benchmark Methodology



Two benchmark families were used. The large-scale experiment used sparse chain networks with 1,000, 5,000, 10,000, 25,000, and 50,000 vertices. Each graph contained one fewer original edge than vertices and used capacity 10. Edge cost was set to 1 so the same costed graph could be supplied to every solver. Edmonds–Karp and Push–Relabel simply ignored the cost field.



A second experiment used denser directed acyclic graphs with 25, 50, 100, and 200 vertices and an edge probability of 0.15. A fixed seed was used for reproducibility. The benchmark explicitly checked that all solvers received graphs with matching vertex and edge counts and returned the same maximum-flow value.



Runtime was measured with `time.perf\_counter()`. Peak traced memory was measured with `tracemalloc`. The memory measurement included graph construction and solver execution. Every completed flow was passed through the validation layer before its result was accepted. The benchmark produced a CSV comparison table plus runtime, memory, and convergence plots.



\## Results



On the sparse scaling experiment, all algorithms returned a maximum flow of 10. At 1,000 vertices, Edmonds–Karp took 0.015748 seconds, Push–Relabel took 0.032331 seconds, and Min-Cost Max-Flow took 0.033684 seconds. At 10,000 vertices, the times were 0.141461, 0.393430, and 0.275880 seconds respectively. At 50,000 vertices, Edmonds–Karp completed in 0.923425 seconds, Push–Relabel in 1.750802 seconds, and Min-Cost Max-Flow in 1.425586 seconds.



Memory growth was close to linear on the sparse graphs. At 1,000 vertices, peak traced memory was approximately 0.87 to 1.00 MB. At 50,000 vertices, Edmonds–Karp used 45.115 MB, Push–Relabel used 49.266 MB, and Min-Cost Max-Flow used 51.126 MB. This is consistent with the adjacency-list representation because the sparse chain increases edges approximately linearly with vertices.



The denser comparison showed a different pattern. At 25 vertices, all solvers returned a maximum flow of 23. At 50 vertices the shared maximum flow was 55, at 100 vertices it was 152, and at 200 vertices it was 256. Edmonds–Karp required 0.083797 seconds at 200 vertices. Push–Relabel required 1.518519 seconds, while Min-Cost Max-Flow required 1.194348 seconds.



The Min-Cost solver showed the expected additional computational cost on denser networks because every augmentation also requires shortest-path calculations that account for costs. For example, at 100 dense vertices it required 0.125523 seconds compared with 0.005108 seconds for Edmonds–Karp.



\## Interpretation



The most surprising finding was that Edmonds–Karp outperformed Push–Relabel in the large sparse experiment. This does not mean Edmonds–Karp is generally the better large-network algorithm. The benchmark topology matters. A chain contains only one simple source-to-sink route, so Edmonds–Karp can find the needed augmenting path immediately and finish after very little augmentation work. This is far from a difficult case for Edmonds–Karp.



Push–Relabel performs more local bookkeeping because it maintains heights, excess values, an active queue, and relabel operations. That overhead is not rewarded on a graph with such a simple path structure. A more adversarial or highly interconnected max-flow graph could produce a very different ranking.



The benchmark therefore demonstrates two lessons. First, asymptotic complexity alone does not predict observed runtime on every input. Second, benchmarking must describe graph structure rather than reporting size by itself. A 50,000-vertex sparse chain can be easier than a much smaller graph with many interacting paths.



\## Conclusion



The project successfully implemented and validated Edmonds–Karp, Push–Relabel, and Min-Cost Max-Flow in one reusable framework. It also demonstrated how flow models can solve matching, segmentation, and scheduling problems. The final system includes validation, generators, visualization, animation, a CLI, automated tests, and reproducible benchmarks.



The 50,000-vertex experiment confirmed that the adjacency-list implementation can handle large sparse graphs with moderate memory use. The results also showed that the theoretically more advanced algorithm is not automatically the fastest on every topology. For this controlled sparse chain, Edmonds–Karp benefited from the graph’s simple structure. Min-Cost Max-Flow remained practical but paid additional cost for optimization over edge costs. Overall, the project demonstrates both the versatility of flow networks and the importance of matching an algorithm to the structure and requirements of the problem.



\## References



Amakobe, M. (2025). \*Advanced Algorithms: Concepts, Complexity, and Applied Projects\*. Chapter 10: Advanced Graph Algorithms.