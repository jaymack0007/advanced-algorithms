\# Week 9 Approximation Algorithms Report



\## Executive Summary



This project examined approximation and randomized algorithms for optimization problems where finding the exact optimum becomes expensive as input size grows. Five problem families were tested: Vertex Cover, Uncapacitated Facility Location, Set Cover, Metric Traveling Salesman Problem (TSP), and Max-Cut. Each approximation or heuristic algorithm was compared with an exact exhaustive baseline on small instances so solution quality could be measured directly.



The results showed the main tradeoff expected from approximation algorithms. Exact algorithms always returned the optimal answer, but their runtimes increased much faster. Vertex Cover reached its theoretical worst-case ratio of 2.0 on every tested cycle graph. The Facility Location greedy heuristic was optimal on four of five tested sizes and was only about 1.1% above optimal for six facilities. Both deterministic and randomized Set Cover LP rounding matched the exact optimum on every generated instance. MST doubling for Metric TSP produced ratios from 1.000 to 1.288, within its theoretical 2-approximation guarantee. Randomized Max-Cut averaged about 56.6% to 67.6% of optimum, while local search improved those results to about 91.2% to 96.7%.



\## Methodology



All algorithms were implemented in Python and tested before benchmarking. Exact algorithms were used only on small inputs because their purpose was to provide a reliable optimum for comparison. Randomized algorithms were run multiple times so mean solution quality and variance could be measured. Set Cover randomized rounding used 30 trials per input size. Randomized Max-Cut used 100 trials, while Max-Cut local search used 30 trials.



For minimization problems, the approximation ratio was approximate cost divided by optimal cost. A value of 1.0 is optimal, while larger values are worse. For Max-Cut, a maximization problem, the ratio was approximate cut value divided by optimal cut value, so values closer to 1.0 are better.



!\[Approximation Ratios](../benchmarks/results/approx\_ratios.png)



!\[Cost vs Optimal](../benchmarks/results/cost\_vs\_optimal.png)



!\[Randomized Max-Cut Results](../benchmarks/results/randomized\_maxcut\_results.png)



\## Vertex Cover



The Vertex Cover implementation used the standard maximal-matching 2-approximation. The algorithm greedily creates a maximal matching and adds both endpoints of every matching edge to the cover. Since every matching edge must have at least one endpoint in any optimal cover, this algorithm selects at most twice as many vertices as the optimum.



The benchmark used cycle graphs with 4, 6, 8, 10, and 12 vertices. In every case, the approximation ratio was exactly 2.0. For example, the 12-vertex cycle had an optimal cover of size 6 while the approximation returned a cover of size 12. This is still correct because it matches the formal worst-case guarantee.



At 12 vertices, exact exhaustive search took about 0.00619 seconds, while the approximation took about 0.0000065 seconds. The approximation gave up solution quality but achieved a major runtime advantage.



\## Facility Location



The Facility Location algorithm used an add-only greedy heuristic. It begins with the best single facility and continues opening facilities only when doing so reduces total opening plus service cost. Unlike the Vertex Cover and TSP algorithms in this project, this implementation does not claim a formal approximation bound.



The heuristic matched the exact optimum for 3, 4, 5, and 7 facilities. At 6 facilities, the heuristic cost was 512.5885 compared with the optimal cost of 507.0010, giving a ratio of about 1.011. This shows both the usefulness and limitation of greedy methods: they can work extremely well in practice, but a locally attractive choice can prevent a globally optimal solution.



At 7 facilities, exact search required about 0.00545 seconds while the greedy method required about 0.000981 seconds.



\## Set Cover with LP Rounding



The Set Cover implementation first solved a linear programming relaxation. Instead of requiring every decision variable to be exactly 0 or 1, the LP allows fractional values between 0 and 1. Its objective gives a lower bound on the integer optimum. The project then used deterministic and randomized rounding, followed by a repair step when necessary to guarantee complete coverage.



For universe sizes 4, 6, 8, 10, and 12, the LP lower bound equaled the exact integer optimum in every tested instance. Both deterministic and randomized rounding also found the exact optimum each time, so all observed approximation ratios were 1.0.



Randomized Set Cover had zero solution-cost variance across all 30 trials at every size. This does not mean randomized rounding always has zero variance. It means these generated instances led to the same final cost after rounding and repair. Runtime still showed the benefit of approximation. For universe size 8, exact search took about 0.1707 seconds, deterministic rounding took about 0.00275 seconds, and randomized rounding averaged about 0.00158 seconds.



LP rounding is useful because Set Cover supports logarithmic approximation behavior. Scaling and rounding a fractional LP solution provides a polynomial-time path from a lower-bound solution to a feasible integer cover. The empirical results here were better than the general worst case because the tested instances showed no observed integrality gap.



\## Metric TSP



The Metric TSP approximation used MST doubling. First, the algorithm constructs a minimum spanning tree. A doubled traversal has cost at most twice the MST cost. Removing one edge from an optimal TSP tour leaves a spanning tree, so the MST cannot cost more than the optimal tour. The triangle inequality then allows repeated vertices to be shortcut without increasing distance. These facts give a 2-approximation for metric TSP.



The observed ratios were about 1.032, 1.105, 1.150, 1.288, 1.000, and 1.189 for 4 through 9 cities. The worst tested case was 7 cities, where the approximation cost was 297.3186 compared with an optimal cost of 230.8019.



At 9 cities, exact TSP took about 0.642 seconds while MST doubling took about 0.000186 seconds. This gap demonstrates how quickly factorial exact search becomes impractical.



\## Randomized Max-Cut and Local Search



The randomized Max-Cut algorithm independently places every vertex on one of two sides with equal probability. Each edge therefore has a one-half probability of crossing the cut. The expected cut value is half of the total edge count, and because the optimum cannot exceed the total number of edges, the expected solution is at least one-half of optimum.



The experiments were consistent with that guarantee. Mean randomized approximation ratios ranged from 0.5663 to 0.6758. For the 14-vertex graph, the optimum was 31 and the randomized mean was 20.95, giving a ratio of about 0.6758.



Local search substantially improved the random starting solutions. Its mean ratios ranged from about 0.9118 to 0.9667. At 14 vertices, local search improved the mean cut from 20.95 to 28.27. The additional runtime was still below one millisecond on the tested instances.



Randomized Max-Cut variance increased from about 2.25 at 6 vertices to about 9.83 at 14 vertices. Local search generally reduced the effect of weak starting partitions by moving vertices whenever a move improved the cut.



\## Approximation Tradeoffs and PTAS/FPTAS



These experiments show why approximation algorithms are useful when exact optimization is impractical. Exact algorithms give the best possible answer, but their runtimes can grow exponentially or factorially. Approximation algorithms instead trade some optimality for speed and scalability, sometimes with a mathematical guarantee on solution quality.



A Polynomial-Time Approximation Scheme (PTAS) allows the user to choose an accuracy parameter. For a minimization problem, a PTAS can produce a solution within a factor of 1 + epsilon of optimum for any fixed positive epsilon, although runtime may increase sharply as epsilon becomes smaller. A Fully Polynomial-Time Approximation Scheme (FPTAS) also requires runtime to remain polynomial in both input size and 1/epsilon. Not every NP-hard optimization problem admits these schemes.



The Week 9 algorithms show several approaches: fixed 2-approximations for Vertex Cover and Metric TSP, logarithmic-style LP rounding for Set Cover, a one-half expected randomized guarantee for Max-Cut, and a practical Facility Location heuristic without a claimed universal bound.



\## Conclusion



The Week 9 results demonstrate that giving up exact optimality can produce major efficiency gains while still maintaining useful solution quality. Exact search was valuable as a benchmark, but approximation methods remained much faster and usually returned near-optimal solutions.



Set Cover produced optimal rounded solutions on every tested instance. Max-Cut local search consistently improved random cuts to more than 91% of optimum on average. Metric TSP stayed comfortably inside its formal 2-approximation guarantee. Vertex Cover showed that a proven approximation bound can be tight because every tested cycle reached the worst-case ratio of 2.0. Overall, the project demonstrates the practical balance between runtime, scalability, and solution quality that approximation algorithms provide when exact optimization becomes too expensive.



\## References



Cormen, T. H., Leiserson, C. E., Rivest, R. L., \& Stein, C. (2022). \*Introduction to Algorithms\* (4th ed.). MIT Press.



Vazirani, V. V. (2001). \*Approximation Algorithms\*. Springer.

