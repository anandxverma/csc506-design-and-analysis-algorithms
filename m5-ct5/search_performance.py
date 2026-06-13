"""
search_performance.py
Compares hash table O(1) average-case lookup against O(n) linear search
on the same 120-item student dataset used in test_data_structures.py.

Measures time per lookup for:
  - Hash table: HashTable.get()
  - Linear search: sequential scan of a plain list
across three target positions: first item, middle item, last item.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))
from hash_table import HashTable

# ---------------------------------------------------------------------------
# Dataset (same 120 records as test_data_structures.py)
# ---------------------------------------------------------------------------

STUDENT_RECORDS = [
    (f"student_{i:03d}", {"id": i, "name": f"Student {i}", "gpa": round(2.0 + (i % 20) * 0.1, 1)})
    for i in range(1, 121)
]

TRIALS = 100_000   # repeat each lookup this many times for stable timing

# ---------------------------------------------------------------------------
# Build structures
# ---------------------------------------------------------------------------

ht = HashTable(size=20)
for key, value in STUDENT_RECORDS:
    ht.insert(key, value)

flat_list = list(STUDENT_RECORDS)   # list of (key, value) tuples

# ---------------------------------------------------------------------------
# Benchmark helpers
# ---------------------------------------------------------------------------

def time_hash_lookup(target_key):
    start = time.perf_counter()
    for _ in range(TRIALS):
        ht.get(target_key)
    return (time.perf_counter() - start) / TRIALS


def time_linear_search(target_key):
    start = time.perf_counter()
    for _ in range(TRIALS):
        for k, v in flat_list:
            if k == target_key:
                break
    return (time.perf_counter() - start) / TRIALS

# ---------------------------------------------------------------------------
# Run comparisons
# ---------------------------------------------------------------------------

targets = [
    ("First item  (best case for linear)",  "student_001"),
    ("Middle item (avg case for linear)",   "student_060"),
    ("Last item   (worst case for linear)", "student_120"),
]

print("=" * 65)
print(f" Search Performance: Hash Table vs. Linear Search")
print(f" Dataset: {len(STUDENT_RECORDS)} records  |  Trials per lookup: {TRIALS:,}")
print("=" * 65)
print(f"{'Scenario':<40} {'Hash (µs)':>10} {'Linear (µs)':>12} {'Speedup':>9}")
print("-" * 65)

for label, key in targets:
    ht_us   = time_hash_lookup(key)   * 1e6
    lin_us  = time_linear_search(key) * 1e6
    speedup = lin_us / ht_us if ht_us > 0 else float("inf")
    print(f"{label:<40} {ht_us:>10.3f} {lin_us:>12.3f} {speedup:>8.1f}x")

print("-" * 65)

# Theoretical expectation note
n = len(STUDENT_RECORDS)
print(f"\nExpected complexity:")
print(f"  Hash table  — O(1) average  (independent of n={n})")
print(f"  Linear search — O(n) average  (scans ~{n//2} items on average)")
print(f"\nAt n={n}, linear search should scan ~{n//2} items on average")
print(f"vs. ~1 bucket probe for the hash table.")
