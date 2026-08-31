Week 1 Performance Analysis



Jaymes McKenzie



Methodology



For this assignment, I compared Bubble Sort, Selection Sort, and Insertion Sort. I tested lists with 100, 250, 500, and 1,000 elements using random, sorted, reverse-sorted, and nearly sorted data. Each test used two warm-up runs and five timed runs, and I used the average time for the results.



Testing was done on Windows 11 Pro using an 11th Gen Intel Core i3-1115G4 @ 3.00 GHz with Python 3.14.5. I also ran the pytest test suite and all 28 tests passed.



Results



Random Data







With 1,000 random values, Insertion Sort was the fastest at about 0.015 seconds. Selection Sort took about 0.023 seconds, and Bubble Sort took about 0.040 seconds. All three got slower quickly as the list size increased.



Sorted Data







Sorted data showed the biggest difference. Bubble Sort took about 0.000042 seconds and Insertion Sort about 0.000074 seconds at 1,000 elements. Selection Sort took about 0.015 seconds.



Bubble Sort was very fast because it stops early when it makes a full pass without any swaps. Insertion Sort also does well when the list is already in order.



Reverse-Sorted Data







Reverse-sorted data was harder for Bubble Sort and Insertion Sort. At 1,000 elements, Bubble Sort took about 0.043 seconds, Insertion Sort took about 0.030 seconds, and Selection Sort took about 0.016 seconds.



This matched the expected slower behavior for these algorithms.



Nearly Sorted Data







Insertion Sort did especially well with nearly sorted data. At 1,000 elements it took about 0.002 seconds, compared with about 0.015 seconds for Selection Sort and 0.021 seconds for Bubble Sort.



This showed that the starting order of the data can make a big difference.



Conclusion



The results mostly matched what I expected from the three sorting algorithms. Bubble Sort did very well when the data was already sorted because of its early-stop check. Selection Sort was more consistent, but it still did the same basic search even when the list was already sorted. Insertion Sort worked especially well with sorted and nearly sorted data.



Overall, the assignment helped show how both list size and the starting order of the data affect how long a sorting algorithm takes.

