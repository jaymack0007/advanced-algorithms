\# Week 5 Dynamic Programming Performance Report



Jaymes McKenzie



\## Executive Summary



Dynamic programming improves problems that would otherwise repeat the same work many times. The main idea is to recognize overlapping subproblems and store results so they can be reused instead of recalculated. This project compared naive recursion, top-down memoization, and bottom-up tabulation using three common problems: Fibonacci, 0/1 Knapsack, and Longest Common Subsequence (LCS).



The benchmark results showed a clear difference between recursive and dynamic programming approaches as input size increased. Naive recursion worked acceptably on small inputs, but its execution time and number of function calls increased very quickly. Memoization reduced repeated calculations by storing results from earlier recursive calls. Tabulation avoided recursion completely and built solutions from smaller values upward.



The most dramatic example was Fibonacci at n = 30. Naive recursion required 2,692,537 calls and took about 0.830 seconds. Memoization completed the same calculation in about 0.000035 seconds, while tabulation took about 0.000006 seconds. Similar improvements appeared in Knapsack and LCS. These results demonstrated why dynamic programming is useful when a problem contains overlapping subproblems and optimal substructure.



\## Methodology



The project was developed and tested on Windows 11 Pro using an 11th Generation Intel Core i3 processor running at approximately 3.00 GHz. Python 3.14.5 was used for the implementations. Pytest was used for automated testing, Pandas was used to store benchmark results, Matplotlib was used for visualization, and Python's `tracemalloc` module was used to measure peak additional memory during each benchmark.



Three versions of Fibonacci were implemented: naive recursion, top-down memoization, and bottom-up tabulation. Input values were 10, 20, 30, 35, 40, and 45. Because naive Fibonacci has exponential time complexity, actual recursive timing was stopped after n = 30. For n = 35, 40, and 45, the program recorded the exact theoretical recursive call count but marked the timing as skipped instead of reporting an estimated execution time.



The Knapsack benchmark used item counts of 5, 10, 15, 20, 30, and 40. The recursive version was measured through 15 items, while both dynamic programming versions continued through 40 items. The input weights and values were generated deterministically so that the same benchmark data could be reproduced.



LCS used string lengths of 10, 50, 100, 250, 500, and 1,000 characters. Naive recursion was only measured at length 10 because larger values grow exponentially. Memoization and tabulation were tested throughout the complete range. For all three problems, execution time, memory use, recursive calls, recursion depth, and available speedup values were recorded.



\## Results



\### Fibonacci



Fibonacci produced the clearest example of exponential growth. At n = 10, naive recursion used 177 calls and took approximately 0.000436 seconds. At n = 20, the call count increased to 21,891 and execution time increased to about 0.005704 seconds. At n = 30, the recursive algorithm required 2,692,537 calls and approximately 0.830142 seconds.



The dynamic programming implementations increased much more slowly. At n = 30, memoization took about 0.000035 seconds and used 59 calls. Tabulation completed the same input in about 0.000006 seconds without recursive calls. Compared with naive recursion, memoization was approximately 23,718 times faster at n = 30, while tabulation was approximately 138,357 times faster in this benchmark.



The theoretical recursive call counts also show why larger naive inputs were not executed. Fibonacci at n = 35 would require 29,860,703 calls, n = 40 would require 331,160,281 calls, and n = 45 would require 3,672,623,805 calls. These values show the expected exponential behavior of the naive solution compared with the O(n) dynamic programming versions.



!\[Fibonacci Comparison](../benchmarks/results/fibonacci\_comparison.png)



\### 0/1 Knapsack



The Knapsack results showed that dynamic programming has some setup overhead on very small problems but becomes much more effective as the input increases. At five items, naive recursion took approximately 0.000086 seconds, while memoization took about 0.000988 seconds. At this small size, recursion was faster than memoization because the problem did not yet contain enough repeated work to overcome the overhead of the memo table and recursive bookkeeping.



The result changed as the number of items increased. At 10 items, naive recursion took about 0.000947 seconds compared with 0.000182 seconds for memoization and 0.000097 seconds for tabulation. At 15 items, naive recursion required 10,434 calls and took approximately 0.030097 seconds. Memoization reduced this to about 0.000488 seconds, while tabulation took about 0.000083 seconds.



The dynamic programming versions continued to handle larger inputs. At 40 items, memoization took about 0.004196 seconds and tabulation took about 0.000687 seconds. The expected DP complexity is O(n × W), where n is the number of items and W is the knapsack capacity. Instead of testing every possible subset, the DP solutions reuse previously calculated item-capacity combinations.



!\[Knapsack Performance](../benchmarks/results/knapsack\_performance.png)



\### Longest Common Subsequence



LCS also showed a major difference between recursion and dynamic programming. At string length 10, naive recursion used 1,941 calls and took about 0.000679 seconds. Memoization reduced the work to 116 calls and approximately 0.000145 seconds. Tabulation completed the same input in about 0.000033 seconds.



The larger LCS results also showed a noticeable difference between the two dynamic programming approaches. At length 250, memoization took approximately 0.310204 seconds and used about 6.61 MB of peak additional memory. Tabulation completed the same size in about 0.008922 seconds and used about 0.52 MB.



At length 1,000, memoization required approximately 29.512806 seconds, 1,252,522 calls, and about 128.67 MB of peak additional memory. Tabulation completed the same input in approximately 1.414453 seconds and used about 12.00 MB. Both methods have an expected time complexity of O(n × m), but the measurements show that implementation details can still produce substantial practical differences.



!\[LCS Performance](../benchmarks/results/lcs\_performance.png)



\## Discussion



Dynamic programming outperformed naive recursion because it prevented the repeated calculation of the same subproblems. Fibonacci demonstrates this especially well. The naive recursive tree calculates the same Fibonacci values many times, causing exponential growth. Memoization keeps the recursive structure but stores each result for later use. Tabulation removes the recursion and calculates each needed value in order.



Memoization and tabulation solve the same type of repeated-work problem, but they use different approaches. Memoization is top-down. It begins with the original problem and recursively calculates only the states that are needed. This can make it easier to convert an existing recursive algorithm into a dynamic programming solution. However, it still has function-call overhead and consumes recursion stack space.



Tabulation is bottom-up. It begins with base cases and fills a table until it reaches the final answer. This usually avoids recursion overhead and recursion-depth limitations. In these benchmarks, tabulation was generally the fastest version. This was especially noticeable in LCS, where the memoized solution at length 1,000 was much slower and used considerably more memory than the tabulated implementation.



The results also demonstrate the importance of optimal substructure. Fibonacci values are built from smaller Fibonacci values, Knapsack solutions depend on optimal solutions for smaller capacities and item sets, and LCS solutions depend on optimal subsequences of smaller string prefixes. Because these larger solutions can be constructed from smaller optimal solutions, previously calculated results can be reused.



Memory is one trade-off of dynamic programming. Storing results requires additional space that naive recursion may not use in the same way. However, recursion also consumes stack space, and repeated calls can become impractical long before the DP table becomes too large. In the tested problems, the additional memory cost of dynamic programming provided a major reduction in execution time.



\## Conclusion



Week 5 demonstrated how dynamic programming transforms inefficient recursive solutions into practical algorithms. Naive recursion was simple to understand but became increasingly expensive as overlapping subproblems multiplied. Memoization improved recursive solutions by caching previously calculated results, while tabulation solved the same problems iteratively from the bottom up.



Fibonacci showed the strongest exponential difference, Knapsack demonstrated optimization under a capacity constraint, and LCS showed how dynamic programming can scale to substantially larger strings. The benchmark results generally matched the expected theoretical behavior: naive approaches grew exponentially, while the dynamic programming solutions followed linear or polynomial growth.



Overall, the project showed that recognizing overlapping subproblems and optimal substructure is the key to applying dynamic programming. It also showed that two algorithms with the same theoretical complexity can still have meaningful differences in runtime, memory use, and implementation overhead.



\## References



Amakobe, M. (2025). \*Advanced Algorithms: A Journey Through Computational Problem Solving\*. Chapter 6: Dynamic Programming, Sections 6.1-6.4.



Cormen, T. H., Leiserson, C. E., Rivest, R. L., \& Stein, C. \*Introduction to Algorithms\* (4th ed.).

