# Week 11 — String Search Engine

This project implements and compares several string-search algorithms from Chapter 32 of *Introduction to Algorithms*:

- Knuth-Morris-Pratt (KMP)

- Rabin-Karp

- Suffix Array with Kasai LCP

- Compressed Suffix Tree / Suffix Trie

- Unified StringSearchEngine interface

The project also includes practical applications, visualization tools, synthetic-data generators, benchmarks, and automated tests.

## Project Structure

```text

StringSearchEngine/

├── core/

│   ├── kmp.py

│   ├── rabin_karp.py

│   ├── suffix_array.py

│   ├── suffix_tree.py

│   └── search_engine.py

├── applications/

│   ├── plagiarism.py

│   ├── dna_search.py

│   └── autocomplete.py

├── visualization/

│   ├── plot_suffix_array.py

│   └── draw_suffix_tree.py

├── utils/

│   ├── text_loader.py

│   ├── rolling_hash.py

│   └── generators.py

├── benchmarks/

│   ├── benchmark_search.py

│   └── results/

│       ├── benchmark_results.csv

│       ├── collision_results.csv

│       ├── sa_lcp_stats.csv

│       ├── runtime_comparison.png

│       ├── collision_analysis.png

│       ├── sa_lcp_stats.png

│       └── heatmap_dataset_sizes.png

└── analysis/

    └── chapter11_report.md

```

## Core Algorithms

### Knuth-Morris-Pratt

The KMP implementation builds the longest-prefix-suffix (LPS) table and uses mismatch fallback positions instead of restarting the search. It supports overlapping matches and provides optional tracing for comparisons and fallbacks.

### Rabin-Karp

Rabin-Karp uses a polynomial rolling hash with configurable base and modulus values. Hash matches are always verified against the actual substring so collisions cannot create false matches.

The implementation also supports multi-pattern searching by grouping patterns of equal length.

### Suffix Array and LCP

The suffix array uses prefix doubling with integer ranks and stable counting sort. Kasai's algorithm constructs the LCP array.

A reusable `SuffixArrayIndex` supports repeated substring searches without rebuilding or revalidating the index for each query.

### Compressed Suffix Tree

The suffix-tree implementation uses the assignment-approved compressed suffix-trie approach rather than Ukkonen's algorithm.

It supports:

- Exact substring search

- Prefix matching

- Longest repeated substring

- Distinct substring counting

- Structural statistics

- Visualization

Because this implementation explicitly inserts suffixes and uses Python object structures, it is intended primarily for smaller educational datasets.

## Unified Search Interface

Example:

```python

from StringSearchEngine.core.search_engine import StringSearchEngine

engine = StringSearchEngine("banana")

result = engine.find(

    "ana",

    method="kmp",

)

print(result.positions)

```

Available methods are:

```text

kmp

rk

sa

tree

```

Suffix-array and suffix-tree indexes are created lazily so preprocessing occurs only when those methods are requested.

## Applications

### Plagiarism Detection

The plagiarism module combines overlapping word shingles with Rabin-Karp matching and suffix-array/LCP analysis.

It provides:

- Document normalization

- Phrase matching

- Similarity scoring

- Longest common substring

- Matched-region highlighting

### DNA Sequence Search

The DNA module provides:

- DNA normalization

- FASTA parsing

- FASTA file loading

- Suffix-array searching

- Suffix-tree searching

- Multiple-pattern searches

- Longest repeated DNA sequence discovery

### Autocomplete

The autocomplete module provides:

- Prefix lookup

- Top-k suggestions

- Frequency-based ranking

- Alphabetical tie breaking

- Dynamic frequency updates

## Visualization

The project can visualize:

- Suffix-array positions

- LCP values

- Compressed suffix-tree structure

Matplotlib uses the noninteractive Agg backend so figures can be generated without requiring a GUI.

## Benchmark

Run the complete benchmark with:

```powershell

python -m StringSearchEngine.benchmarks.benchmark_search

```

A smaller validation benchmark is available with:

```powershell

python -m StringSearchEngine.benchmarks.benchmark_search --smoke

```

The official benchmark compares a 10 KB dataset and a 1 MB dataset.

### Final Results

| Dataset | Algorithm | Preprocessing | Average Search | Persistent Index |

|---|---:|---:|---:|---:|

| 10 KB | KMP | 0.000 s | 1.398 ms | 0.000 MB |

| 10 KB | Rabin-Karp | 0.000 s | 7.361 ms | 0.000 MB |

| 10 KB | Suffix Array | 0.060 s | 0.010 ms | 0.430 MB |

| 10 KB | Suffix Tree | 0.075 s | 0.021 ms | 53.572 MB |

| 1 MB | KMP | 0.000 s | 217.998 ms | 0.000 MB |

| 1 MB | Rabin-Karp | 0.000 s | 688.388 ms | 0.000 MB |

| 1 MB | Suffix Array | 18.321 s | 0.018 ms | 42.916 MB |

| 1 MB | Suffix Tree | Skipped | Skipped | Skipped |

All algorithms that were executed found the same three expected pattern occurrences.

The compressed suffix tree was intentionally skipped on the 1 MB dataset because the assignment-approved Option A implementation has high memory overhead and does not scale appropriately to that input size.

## Rabin-Karp Collision Experiment

The collision experiment demonstrates how modulus size affects false hash matches.

| Modulus | Collisions |

|---:|---:|

| 5 | 3,980 |

| 17 | 1,143 |

| 101 | 169 |

| 1,009 | 30 |

| 10,007 | 1 |

| 1,000,000,007 | 0 |

Every hash hit is verified against the source text, so collisions do not affect correctness.

## Testing

Run all repository tests with:

```powershell

python -m pytest .\\tests -q

```

Final verified result:

```text

1008 passed

```

The complete analysis is available in:

```text

StringSearchEngine/analysis/chapter11_report.md

```
