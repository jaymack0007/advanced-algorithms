# Chapter 11 String Search Engine Analysis Report

## Executive Summary

This project implemented and evaluated four string-search approaches: Knuth-Morris-Pratt (KMP), Rabin-Karp, suffix arrays with a longest-common-prefix (LCP) array, and a compressed suffix tree. The goal was not only to produce correct pattern matching, but also to compare the tradeoffs between algorithms that scan the text for each query and indexed approaches that perform preprocessing before repeated searches. The project also included practical applications for plagiarism detection, DNA sequence search, and autocomplete, along with visualizations and synthetic benchmark generators.

All Week 11 components were integrated into the existing Advanced Algorithms repository and the complete repository test suite finished with 1,008 passing tests. The final benchmark used a 10,000-character small dataset and a 1,000,000-character medium dataset. Each dataset contained the same benchmark pattern at three known locations so correctness could be checked across algorithms. KMP was the fastest non-indexed method. Rabin-Karp was slower in this Python implementation, but its rolling hash supported multi-pattern searching and provided useful collision analysis. The suffix array required substantial preprocessing, especially at 1 MB, but once built it produced the lowest repeated-query latency. The compressed suffix tree also provided extremely fast queries, but its memory cost was high, so it was intentionally limited to the small dataset.

## Methodology

The KMP implementation first constructs the LPS table and then uses fallback positions instead of restarting after a mismatch. This gives deterministic O(n + m) search time for text length n and pattern length m. The implementation supports overlapping matches, empty patterns, Unicode text, and detailed tracing of comparisons and fallbacks.

Rabin-Karp uses a polynomial rolling hash. A window hash is updated in constant time as the search moves through the text, and every hash match is verified against the actual substring so collisions cannot create false results. The implementation also supports multiple patterns by grouping patterns of equal length and scanning the text once for each distinct length. Collision statistics are recorded so the effect of the modulus can be measured directly.

The suffix-array implementation uses prefix doubling with integer ranks and stable counting sort. The LCP array is produced with Kasai's algorithm. Pattern searches use two binary searches to find the matching suffix interval. A reusable SuffixArrayIndex stores both the suffix array and LCP array so validation and construction are not repeated for every query.

For the suffix tree, the project used the assignment-approved compressed suffix-trie option instead of Ukkonen's algorithm. Every suffix is inserted into a radix-style tree and common prefixes are compressed into labeled edges. This version is easy to inspect and visualize, but its explicit suffix insertion can require quadratic construction work and large Python-object overhead. For that reason, the benchmark used the tree on the 10 KB dataset but skipped it on the 1 MB dataset rather than risking an unrepresentative or excessive run.

Preprocessing time was measured separately from query time. KMP and Rabin-Karp have no persistent index, while the suffix array and suffix tree retain data structures between searches. Persistent index memory was therefore estimated separately from temporary peak query memory. This avoided using memory tracing during large suffix-array construction, which had previously distorted preprocessing time.

## Benchmark Results

The final runtime measurements are shown below.

| Dataset | Algorithm | Preprocessing (s) | Avg. Search (ms) | Persistent Index (MB) | Matches |

|---|---:|---:|---:|---:|---:|

| 10 KB | KMP | 0.000 | 1.398 | 0.000 | 3 |

| 10 KB | Rabin-Karp | 0.000 | 7.361 | 0.000 | 3 |

| 10 KB | Suffix Array | 0.060 | 0.010 | 0.430 | 3 |

| 10 KB | Suffix Tree | 0.075 | 0.021 | 53.572 | 3 |

| 1 MB | KMP | 0.000 | 217.998 | 0.000 | 3 |

| 1 MB | Rabin-Karp | 0.000 | 688.388 | 0.000 | 3 |

| 1 MB | Suffix Array | 18.321 | 0.018 | 42.916 | 3 |

| 1 MB | Suffix Tree | Skipped | Skipped | Skipped | — |

All executed algorithms returned exactly the three expected match positions. The results show the central tradeoff of indexed string searching. KMP required no preprocessing and remained efficient for a one-time query, but its cost grew with the size of the text because it scans the text for each pattern. Rabin-Karp also scans the text and was slower than KMP in these tests because Python-level rolling-hash updates add overhead. That result does not make Rabin-Karp incorrect or generally inferior; its main advantage in this project is reusable hashing for batch searches and collision experiments.

The suffix array paid a large preprocessing cost. Construction increased from about 0.060 seconds at 10 KB to 18.321 seconds at 1 MB. However, once the index existed, average query time was only about 0.010 ms at 10 KB and 0.018 ms at 1 MB. This makes the suffix array attractive when the same text will receive many searches. Its persistent memory also scaled substantially, from approximately 0.43 MB at 10 KB to 42.92 MB at 1 MB.

The compressed suffix tree demonstrated even faster direct navigation than scanning methods, with an average search time of about 0.021 ms on the 10 KB dataset. Its major weakness was memory. The Python object representation occupied about 53.57 MB for only 10 KB of text. This is a consequence of using the simpler compressed suffix-trie construction and individual dictionaries, nodes, edge objects, strings, and suffix positions. The 1 MB tree benchmark was therefore skipped intentionally. A production suffix tree would need a more memory-efficient representation or an online linear-time construction such as Ukkonen's algorithm.

## Collision and LCP Analysis

The Rabin-Karp collision experiment clearly showed why modulus selection matters. With modulus 5, the search produced 3,980 false hash collisions. Modulus 17 reduced this to 1,143, modulus 101 to 169, modulus 1,009 to 30, and modulus 10,007 to one. With modulus 1,000,000,007, there were zero false collisions and exactly one true hash hit for the inserted test pattern. Because every hash hit is verified with direct string comparison, correctness was preserved even with very small moduli, but poor modulus choices created unnecessary verification work.

The LCP results also reflected dataset growth. Mean LCP increased from approximately 2.17 characters at 10 KB to 3.56 characters at 1 MB, while the maximum LCP remained 19 characters in both datasets. This indicates that a larger random dataset naturally created more short shared prefixes among neighboring suffixes, while the longest observed shared prefix did not increase in this controlled benchmark.

## Applications and Algorithm Selection

The plagiarism application combines overlapping word shingles with Rabin-Karp matching and uses a suffix array plus LCP information to identify a longest common substring between two documents. This demonstrates how hashing is useful for repeated phrase detection while suffix indexing supports deeper structural similarity.

The DNA application normalizes sequences, parses FASTA records, and supports exact searches with either a suffix array or suffix tree. A suffix array is the more practical default for larger sequences in this implementation because its memory use is much lower than the compressed suffix tree. The autocomplete application uses a prefix index with frequency weighting and top-k ranking, illustrating a related prefix-search problem without forcing a suffix structure where a simpler prefix index is more appropriate.

For one or a small number of searches against a text, KMP is the strongest default because it requires no preprocessing, has deterministic linear complexity, and used very little additional memory. Rabin-Karp is most useful when hashing, batch pattern matching, or collision analysis is important. For many searches against the same static text, the suffix array is the best overall indexed choice in this project. The compressed suffix tree gives excellent lookup speed but is best treated as an educational structure for small inputs unless its construction and representation are replaced with a more scalable implementation.

## Conclusion

The project demonstrates that algorithm selection depends on workload rather than search speed alone. KMP performed well for direct searches because it avoids preprocessing and guarantees linear-time matching. Rabin-Karp added flexible rolling-hash behavior and showed experimentally how modulus size controls collision frequency. The suffix array required the greatest practical preprocessing investment on the large dataset, but it converted later searches into extremely fast binary-search queries while maintaining a manageable index compared with the suffix tree.

The compressed suffix tree successfully demonstrated prefix compression, repeated-substring discovery, and fast indexed lookup, but its memory results also showed the limitations of the assignment's simpler construction strategy. Overall, the benchmark supports using KMP for occasional searches and a suffix array when many queries will reuse the same text. The applications further show that string algorithms are not interchangeable: different workloads benefit from different combinations of scanning, hashing, suffix indexing, and prefix-based data structures.
