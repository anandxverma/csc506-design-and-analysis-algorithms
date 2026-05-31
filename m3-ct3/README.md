# Sorting Algorithm Benchmark

Benchmarks four classical sorting algorithms across multiple dataset types and sizes, then produces an analysis report comparing their performance.

# Source Code
The source code is available for download from Github at https://github.com/anandxverma/csc506-design-and-analysis-algorithms/tree/main/m3-ct3

## Algorithms

| Algorithm | Time Complexity | Notes |
|---|---|---|
| Bubble Sort | O(n²) | Teaching example; skipped at n ≥ 50,000 |
| Insertion Sort | O(n²) | Best O(n²) on small or nearly-sorted data |
| Selection Sort | O(n²) | O(n) swaps; skipped at n ≥ 50,000 |
| Merge Sort | O(n log n) | Best general-purpose choice |

## Dataset Types

| Type | Description |
|---|---|
| `random` | Uniformly shuffled integers (average case) |
| `sorted` | Ascending order (best case for many algorithms) |
| `reverse_sorted` | Descending order (worst case for bubble/insertion) |
| `partially_sorted` | ~80% sorted with random swaps (near-best case) |

## Sizes

`1,000 · 5,000 · 10,000 · 50,000`

O(n²) algorithms are automatically skipped at n = 50,000 to avoid multi-minute runtimes.

## Files

```
benchmark.py        Main entry point — runs benchmarks and prints analysis
bubble_sort.py      Bubble sort implementation
insertion_sort.py   Insertion sort implementation
selection_sort.py   Selection sort implementation
merge_sort.py       Merge sort implementation
data_generator.py   Dataset generators (random, sorted, reverse, partial)
```

## Usage

```bash
python benchmark.py
```

The program prints:

1. **Benchmark table** — time (seconds) and pass/fail for every algorithm × dataset × size combination
2. **Best Algorithm per Scenario** — fastest algorithm for each (dataset, size) pair with gap to runner-up
3. **Algorithm Win Summary** — win count and win percentage per algorithm
4. **Recommendation guide** — plain-English guidance on when to use each algorithm

At the end, you are prompted to optionally export the raw results to a CSV file.

## Example Output (truncated)

```
Sorting Algorithm Benchmark
================================================================
Algorithm       Dataset            Size    Time (s)  Status
----------------------------------------------------------------
Bubble Sort     random             1000    0.034521  OK
Bubble Sort     random             5000    0.892014  OK
...
Merge Sort      random            50000    0.031887  OK
```
