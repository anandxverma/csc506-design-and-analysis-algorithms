"""
Performance Analysis: Tree-Based Map vs. List-Based Map — Search Operations
============================================================================
Compares the BST-backed Map (bst.py) against a naive ListMap across:
  - Dataset sizes : 100, 500, 1_000, 5_000, 10_000
  - Insertion order: random-shuffled (avg-case BST) and sorted (worst-case BST)
  - Search type    : hit  (key exists)  and  miss (key absent)

Theoretical complexity
  ListMap.get   — O(n)        sequential scan
  Map.get       — O(log n)    balanced BST (random insertion)
  Map.get       — O(n)        degenerate BST (sorted insertion → right-skewed chain)
"""

import random
import time
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
sys.setrecursionlimit(20_000)   # sorted BST chains are O(n) deep
from bst import Map


# ---------------------------------------------------------------------------
# List-backed map
# ---------------------------------------------------------------------------

class ListMap:
    """
    Unordered map backed by a list of (key, value) pairs.

    put / get / contains_key all perform a full linear scan: O(n).
    """

    def __init__(self):
        self._data = []

    def put(self, key, value):
        for i, (k, _) in enumerate(self._data):
            if k == key:
                self._data[i] = (key, value)
                return
        self._data.append((key, value))

    def get(self, key):
        for k, v in self._data:
            if k == key:
                return v
        raise KeyError(key)

    def contains_key(self, key):
        for k, _ in self._data:
            if k == key:
                return True
        return False


# ---------------------------------------------------------------------------
# Benchmark helpers
# ---------------------------------------------------------------------------

REPEATS = 500   # searches per timing sample


def _time_searches(map_obj, keys_to_search, repeats):
    """Return total elapsed seconds for `repeats` full passes over keys_to_search."""
    start = time.perf_counter()
    for _ in range(repeats):
        for k in keys_to_search:
            map_obj.contains_key(k)
    return time.perf_counter() - start


def build_maps(keys, values):
    """Populate a fresh TreeMap and ListMap with the same key-value pairs."""
    tree_map = Map()
    list_map = ListMap()
    for k, v in zip(keys, values):
        tree_map.put(k, v)
        list_map.put(k, v)
    return tree_map, list_map


def run_benchmark(size, order):
    """
    Run one benchmark scenario.

    Parameters
    ----------
    size  : number of entries in each map
    order : 'random' | 'sorted'

    Returns
    -------
    dict with timing and ratio results.
    """
    base_keys = list(range(size))
    values    = [f"val_{k}" for k in base_keys]

    if order == "sorted":
        insert_keys = base_keys              # worst-case for BST
    else:
        insert_keys = base_keys[:]
        random.shuffle(insert_keys)

    tree_map, list_map = build_maps(insert_keys, values)

    # --- hit searches: keys that exist ---
    hit_sample = random.sample(base_keys, min(50, size))
    tree_hit = _time_searches(tree_map, hit_sample, REPEATS)
    list_hit = _time_searches(list_map, hit_sample, REPEATS)

    # --- miss searches: keys that do NOT exist ---
    miss_keys = [size + i for i in range(50)]
    tree_miss = _time_searches(tree_map, miss_keys, REPEATS)
    list_miss = _time_searches(list_map, miss_keys, REPEATS)

    total_searches = 50 * REPEATS

    def per_search_us(elapsed):
        return (elapsed / total_searches) * 1e6   # microseconds

    return {
        "size":         size,
        "order":        order,
        "tree_hit_us":  per_search_us(tree_hit),
        "list_hit_us":  per_search_us(list_hit),
        "tree_miss_us": per_search_us(tree_miss),
        "list_miss_us": per_search_us(list_miss),
        "hit_ratio":    list_hit  / tree_hit  if tree_hit  > 0 else float("inf"),
        "miss_ratio":   list_miss / tree_miss if tree_miss > 0 else float("inf"),
    }


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

SIZES = [100, 500, 1_000, 5_000, 10_000]

COL = {
    "size":         10,
    "order":         8,
    "tree_hit":     14,
    "list_hit":     14,
    "tree_miss":    14,
    "list_miss":    14,
    "hit_ratio":    12,
    "miss_ratio":   12,
}

HEADER = (
    f"{'n':>{COL['size']}} "
    f"{'order':<{COL['order']}} "
    f"{'tree-hit(µs)':>{COL['tree_hit']}} "
    f"{'list-hit(µs)':>{COL['list_hit']}} "
    f"{'tree-miss(µs)':>{COL['tree_miss']}} "
    f"{'list-miss(µs)':>{COL['list_miss']}} "
    f"{'hit-ratio':>{COL['hit_ratio']}} "
    f"{'miss-ratio':>{COL['miss_ratio']}}"
)

SEP = "-" * len(HEADER)


def print_report(results):
    print("\n" + "=" * len(HEADER))
    print("PERFORMANCE ANALYSIS: Tree-Based Map vs. List-Based Map (Search)")
    print(f"  Each cell: avg µs per contains_key() call  |  repeats={REPEATS}  |  sample=50 keys")
    print(f"  hit-ratio / miss-ratio = list_time / tree_time  (>1 means BST is faster)")
    print("=" * len(HEADER))
    print(HEADER)
    print(SEP)

    prev_order = None
    for r in results:
        if prev_order is not None and r["order"] != prev_order:
            print(SEP)
        prev_order = r["order"]

        print(
            f"{r['size']:>{COL['size']},} "
            f"{r['order']:<{COL['order']}} "
            f"{r['tree_hit_us']:>{COL['tree_hit']}.4f} "
            f"{r['list_hit_us']:>{COL['list_hit']}.4f} "
            f"{r['tree_miss_us']:>{COL['tree_miss']}.4f} "
            f"{r['list_miss_us']:>{COL['list_miss']}.4f} "
            f"{r['hit_ratio']:>{COL['hit_ratio']}.2f}x "
            f"{r['miss_ratio']:>{COL['miss_ratio']}.2f}x"
        )

    print("=" * len(HEADER))
    _print_analysis(results)


def _print_analysis(results):
    print("\nANALYSIS")
    print("-" * 60)

    random_results = [r for r in results if r["order"] == "random"]
    sorted_results = [r for r in results if r["order"] == "sorted"]

    # Growth rate: ratio of time at 10x the size
    print("\n[1] Complexity growth — random-insertion BST (expected O(log n) vs O(n))")
    print(f"    {'n1':>6}  {'n2':>7}  {'tree growth':>14}  {'list growth':>14}  {'log₂ ratio':>12}")
    for i in range(1, len(random_results)):
        r1, r2 = random_results[i - 1], random_results[i]
        tree_growth = r2["tree_hit_us"] / r1["tree_hit_us"]
        list_growth = r2["list_hit_us"] / r1["list_hit_us"]
        import math
        log_ratio   = math.log2(r2["size"]) / math.log2(r1["size"])
        print(f"    {r1['size']:>6,} → {r2['size']:>6,}  "
              f"{tree_growth:>14.2f}x  {list_growth:>14.2f}x  {log_ratio:>12.2f}")

    print("\n[2] Complexity growth — sorted-insertion BST (expected O(n) vs O(n))")
    print(f"    {'n1':>6}  {'n2':>7}  {'tree growth':>14}  {'list growth':>14}")
    for i in range(1, len(sorted_results)):
        r1, r2 = sorted_results[i - 1], sorted_results[i]
        tree_growth = r2["tree_hit_us"] / r1["tree_hit_us"]
        list_growth = r2["list_hit_us"] / r1["list_hit_us"]
        print(f"    {r1['size']:>6,} → {r2['size']:>6,}  "
              f"{tree_growth:>14.2f}x  {list_growth:>14.2f}x")

    print("\n[3] Speed advantage of BST (random) over list at each size (hit searches)")
    for r in random_results:
        print(f"    n={r['size']:>6,}  BST is {r['hit_ratio']:.1f}x faster (hit)  "
              f"| {r['miss_ratio']:.1f}x faster (miss)")

    print("\n[4] Sorted-insertion BST vs. list at each size (hit searches)")
    for r in sorted_results:
        print(f"    n={r['size']:>6,}  ratio={r['hit_ratio']:.2f}x  "
              f"(BST degenerates to O(n), approaches list performance)")

    print("\n[5] Theoretical summary")
    print("    Structure          | Insert   | Search (avg) | Search (worst)")
    print("    -------------------|----------|--------------|---------------")
    print("    BST Map (random)   | O(log n) | O(log n)     | O(n)")
    print("    BST Map (sorted)   | O(n)     | O(n)         | O(n)")
    print("    List Map           | O(n)     | O(n)         | O(n)")
    print()
    print("    Key takeaway: a randomly-built BST dominates the list at all sizes.")
    print("    Sorted insertion collapses the BST into a linked-list chain, closing")
    print("    the performance gap entirely — use a self-balancing tree (AVL/Red-Black)")
    print("    if insertion order is not controlled.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    random.seed(42)

    print("Running benchmarks …", flush=True)
    results = []
    for order in ("random", "sorted"):
        for size in SIZES:
            print(f"  {order:8s}  n={size:>6,} … ", end="", flush=True)
            r = run_benchmark(size, order)
            results.append(r)
            print(f"done  (tree-hit={r['tree_hit_us']:.4f} µs, "
                  f"list-hit={r['list_hit_us']:.4f} µs)")

    print_report(results)
