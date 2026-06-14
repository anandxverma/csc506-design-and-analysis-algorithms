# M5-CT5: Hash Table & Priority Queue

CSC506 — Design and Analysis of Algorithms, Module 5 Critical Thinking assignment.

Implements a **hash table with chaining** and a **min-heap priority queue** from scratch, then benchmarks both structures against naive alternatives.

---

## Files

| File | Description |
|------|-------------|
| `hash_table.py` | Hash table using separate chaining for collision resolution |
| `priority_queue.py` | Min-heap based priority queue |
| `test_performance.py` | Performance tests, collision demos, and correctness checks |

---

## Data Structures

### Hash Table (`hash_table.py`)

- **Collision resolution:** separate chaining — each bucket holds a list of `(key, value)` tuples.
- **Hash function:** sums the ASCII values of all characters in the key, then wraps with `mod table_size`.
- **Operations:** `insert`, `get`, `delete` — all average O(1) with a well-sized table.

```python
from hash_table import HashTable

ht = HashTable(size=10)
ht.insert("name", "Alice")
ht.insert("age", 30)
print(ht.get("name"))   # Alice
ht.delete("age")
ht.display_buckets()    # prints non-empty bucket chains
```

### Priority Queue (`priority_queue.py`)

- **Backing store:** binary min-heap (array-based).
- **Ordering:** lowest numeric priority value = highest priority (dequeued first).
- **Operations:** `push` O(log n), `pop` O(log n), `peek` O(1).

```python
from priority_queue import PriorityQueue

pq = PriorityQueue()
pq.push("critical task", priority=1)
pq.push("low urgency task", priority=10)
pq.push("medium task", priority=5)

print(pq.peek())   # critical task
print(pq.pop())    # critical task  (removed)
print(pq.pop())    # medium task
```

---

## Running the Tests

**Hash table standalone demo** (shows deliberate collisions):
```bash
python hash_table.py
```

**Priority queue standalone demo** (processes items in priority order):
```bash
python priority_queue.py
```

**Full performance benchmark** (120-item dataset):
```bash
python test_performance.py
```

The benchmark covers:
1. **HashTable correctness** — insert, spot-check, update, and delete verification on 120 keys.
2. **Collision demonstration** — anagram keys that are guaranteed to hash to the same bucket, showing chained lookup still returns correct values.
3. **Collision performance impact** — overloaded table (size=10) vs. well-sized table (size=150) with the same 120 keys; measures the lookup slowdown caused by long chains.
4. **Hash table vs. linear search** — repeated timed lookups for first, middle, and last items, plus a full-scan comparison across all 120 keys.
5. **PriorityQueue correctness** — verifies that 120 items are popped in strictly ascending priority order.
6. **PriorityQueue performance** — measures push and pop throughput.

---

## Key Concepts Demonstrated

- **Separate chaining** handles hash collisions without probing or rehashing.
- **Anagram collision** — any two keys whose characters are permutations of each other produce identical ASCII sums and therefore land in the same bucket.
- **Load factor effect** — an overloaded table (load factor > 1) degrades lookup toward O(n) as chains grow; a well-sized table keeps chains short and lookup near O(1).
- **Heap invariant** — `_sift_up` after push and `_sift_down` after pop maintain the min-heap property at every step.

---

## Requirements

- Python 3.8+
- No external dependencies
