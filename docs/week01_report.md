\# Week 1 Performance Analysis



\## Jaymes McKenzie



\## Methodology



For this assignment, I tested Bubble Sort, Selection Sort, and Insertion Sort

using the benchmarking framework created for the project.



I tested lists containing 100, 250, 500, and 1,000 elements. The four input

types were random, sorted, reverse sorted, and nearly sorted. Each test used

two warm-up runs followed by five timed runs, and the average execution time

was recorded.



Testing was completed on:



\- Windows 11 Pro

\- 11th Gen Intel Core i3-1115G4 @ 3.00 GHz

\- Python 3.14.5



I also ran the pytest test suite before benchmarking, and all 28 tests passed.



\## Results



\### Random Data



!\[Random Data Performance](../results/random\_performance.png)



At 1,000 elements, Insertion Sort was the fastest at about 0.015 seconds,

followed by Selection Sort at 0.023 seconds and Bubble Sort at 0.040 seconds.

All three showed the expected quadratic growth as the input became larger.



\### Sorted Data



!\[Sorted Data Performance](../results/sorted\_performance.png)



Sorted data produced the biggest difference between the algorithms. Bubble

Sort took about 0.000042 seconds at 1,000 elements and Insertion Sort took

about 0.000074 seconds. Selection Sort took about 0.015 seconds.



Bubble Sort performed very well because the optimized version stops when a

complete pass makes no swaps. Insertion Sort also benefits when the values

are already in order. Selection Sort still searches through the remaining

elements even when the list is already sorted.



\### Reverse-Sorted Data



!\[Reverse Data Performance](../results/reverse\_performance.png)



At 1,000 elements, Bubble Sort took about 0.043 seconds, Insertion Sort took

0.030 seconds, and Selection Sort took about 0.016 seconds.



Reverse order required much more work from Bubble Sort and Insertion Sort.

The benchmark results for all three algorithms were consistent with O(n^2)

behavior in this case.



\### Nearly Sorted Data



!\[Nearly Sorted Data Performance](../results/nearly\_sorted\_performance.png)



Insertion Sort performed especially well on nearly sorted data. At 1,000

elements it took about 0.002 seconds, compared with 0.015 seconds for

Selection Sort and 0.021 seconds for Bubble Sort.



This shows that the organization of the input can have a major effect on

actual performance, even when algorithms have the same worst-case Big-O

complexity.



\## Conclusion



The benchmark results generally matched the expected behavior of the three

sorting algorithms. All three can have O(n^2) behavior, but their actual

performance was different depending on how the input was arranged.



Bubble Sort benefited greatly from its early-exit optimization on sorted

data. Selection Sort was more consistent because it performs its comparisons

regardless of the original ordering. Insertion Sort worked especially well

with sorted and nearly sorted data.



This experiment helped show the difference between theoretical complexity

and measured performance, and why both input size and input organization

matter when comparing algorithms.

