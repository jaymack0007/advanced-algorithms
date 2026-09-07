\# Adv Algo - Week 2 - Master Theorem Exercises



\## Jaymes McKenzie



The Master Theorem can be used for recurrence relations in the form:



T(n) = aT(n/b) + f(n)



where:



\- a = number of subproblems

\- b = factor that reduces the input size

\- f(n) = work done outside the recursive calls



The main step is comparing f(n) with n^(log\_b a).



\---



\## 1. T(n) = 2T(n/2) + n



\- a = 2

\- b = 2

\- f(n) = n

\- n^(log\_2 2) = n



The two terms are the same order.



\*\*Master Theorem Case 2\*\*



\*\*Answer:\*\*



Θ(n log n)



This is the recurrence used by Merge Sort.



\---



\## 2. T(n) = 2T(n/2) + 1



\- a = 2

\- b = 2

\- f(n) = 1

\- n^(log\_2 2) = n



The recursive work grows faster than f(n).



\*\*Master Theorem Case 1\*\*



\*\*Answer:\*\*



Θ(n)



\---



\## 3. T(n) = 4T(n/2) + n



\- a = 4

\- b = 2

\- f(n) = n

\- n^(log\_2 4) = n²



n² grows faster than n.



\*\*Master Theorem Case 1\*\*



\*\*Answer:\*\*



Θ(n²)



\---



\## 4. T(n) = 4T(n/2) + n²



\- a = 4

\- b = 2

\- f(n) = n²

\- n^(log\_2 4) = n²



The terms are the same order.



\*\*Master Theorem Case 2\*\*



\*\*Answer:\*\*



Θ(n² log n)



\---



\## 5. T(n) = 4T(n/2) + n³



\- a = 4

\- b = 2

\- f(n) = n³

\- n^(log\_2 4) = n²



n³ grows faster than n².



\*\*Master Theorem Case 3\*\*



\*\*Answer:\*\*



Θ(n³)



\---



\## 6. T(n) = 3T(n/2) + n



\- a = 3

\- b = 2

\- f(n) = n

\- n^(log\_2 3) ≈ n^1.585



The recursive term grows faster than n.



\*\*Master Theorem Case 1\*\*



\*\*Answer:\*\*



Θ(n^1.585)



\---



\## 7. T(n) = 3T(n/2) + n²



\- a = 3

\- b = 2

\- f(n) = n²

\- n^(log\_2 3) ≈ n^1.585



n² grows faster.



\*\*Master Theorem Case 3\*\*



\*\*Answer:\*\*



Θ(n²)



\---



\## 8. T(n) = T(n/2) + 1



\- a = 1

\- b = 2

\- f(n) = 1

\- n^(log\_2 1) = 1



The terms are the same order.



\*\*Master Theorem Case 2\*\*



\*\*Answer:\*\*



Θ(log n)



\---



\## 9. T(n) = T(n/2) + n



\- a = 1

\- b = 2

\- f(n) = n

\- n^(log\_2 1) = 1



n grows faster than the recursive term.



\*\*Master Theorem Case 3\*\*



\*\*Answer:\*\*



Θ(n)



\---



\## 10. T(n) = 8T(n/2) + n²



\- a = 8

\- b = 2

\- f(n) = n²

\- n^(log\_2 8) = n³



n³ grows faster than n².



\*\*Master Theorem Case 1\*\*



\*\*Answer:\*\*



Θ(n³)



\---



\## 11. T(n) = 8T(n/2) + n³



\- a = 8

\- b = 2

\- f(n) = n³

\- n^(log\_2 8) = n³



The two terms are the same order.



\*\*Master Theorem Case 2\*\*



\*\*Answer:\*\*



Θ(n³ log n)



\---



\## 12. T(n) = 2T(n/4) + √n



\- a = 2

\- b = 4

\- f(n) = √n

\- n^(log\_4 2) = √n



The terms are the same order.



\*\*Master Theorem Case 2\*\*



\*\*Answer:\*\*



Θ(√n log n)



\---



\## Summary



These exercises show the three main Master Theorem cases:



\- \*\*Case 1:\*\* Recursive work dominates.

\- \*\*Case 2:\*\* Recursive work and outside work are balanced.

\- \*\*Case 3:\*\* Work outside the recursion dominates.



The Merge Sort recurrence is especially important for this week's assignment:



T(n) = 2T(n/2) + n



Using the Master Theorem gives:



Θ(n log n)



This matches the theoretical running time for Merge Sort.

