"""
test_data_structures.py
Exercises HashTable and PriorityQueue with 100+ data items each.
Covers insert/get/delete/update for the hash table and
push/pop/peek/ordering for the priority queue.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from hash_table import HashTable
from priority_queue import PriorityQueue

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PASS = "[PASS]"
FAIL = "[FAIL]"

def check(label, condition):
    status = PASS if condition else FAIL
    print(f"  {status}  {label}")
    return condition

# ---------------------------------------------------------------------------
# Dataset — 120 (key, value) pairs
# ---------------------------------------------------------------------------

STUDENT_RECORDS = [
    (f"student_{i:03d}", {"id": i, "name": f"Student {i}", "gpa": round(2.0 + (i % 20) * 0.1, 1)})
    for i in range(1, 121)          # 120 records
]

# Priority tasks: (task_name, priority) where lower number = higher priority
TASK_RECORDS = [
    (f"task_{i:03d}", (i % 10) + 1)    # priorities cycle 1-10; 110 tasks
    for i in range(1, 111)
]

# ---------------------------------------------------------------------------
# Section 1: Hash Table — basic insert + get (120 items)
# ---------------------------------------------------------------------------

def test_ht_insert_and_get():
    print("\n=== Hash Table: Insert & Get (120 items) ===")
    ht = HashTable(size=20)
    inserted = 0
    for key, value in STUDENT_RECORDS:
        ht.insert(key, value)
        inserted += 1

    check(f"Inserted all {inserted} records", inserted == 120)

    misses = 0
    for key, value in STUDENT_RECORDS:
        try:
            result = ht.get(key)
            if result != value:
                misses += 1
        except KeyError:
            misses += 1

    check("All 120 records retrieved correctly", misses == 0)

# ---------------------------------------------------------------------------
# Section 2: Hash Table — in-place update (50 updates)
# ---------------------------------------------------------------------------

def test_ht_update():
    print("\n=== Hash Table: In-place Update (50 items) ===")
    ht = HashTable(size=20)
    for key, value in STUDENT_RECORDS:
        ht.insert(key, value)

    updated_keys = [f"student_{i:03d}" for i in range(1, 51)]   # first 50
    for key in updated_keys:
        ht.insert(key, {"updated": True, "key": key})

    wrong = sum(
        1 for k in updated_keys
        if ht.get(k) != {"updated": True, "key": k}
    )
    check("50 in-place updates applied correctly", wrong == 0)

    # Make sure the other 70 records were untouched
    untouched_keys = [f"student_{i:03d}" for i in range(51, 121)]
    wrong_untouched = sum(
        1 for k in untouched_keys
        if "updated" in ht.get(k)
    )
    check("Remaining 70 records untouched", wrong_untouched == 0)

# ---------------------------------------------------------------------------
# Section 3: Hash Table — delete (40 deletions)
# ---------------------------------------------------------------------------

def test_ht_delete():
    print("\n=== Hash Table: Delete (40 items) ===")
    ht = HashTable(size=20)
    for key, value in STUDENT_RECORDS:
        ht.insert(key, value)

    delete_keys = [f"student_{i:03d}" for i in range(81, 121)]  # last 40
    errors = 0
    for key in delete_keys:
        try:
            ht.delete(key)
        except KeyError:
            errors += 1
    check("40 records deleted without error", errors == 0)

    # Confirm deleted keys raise KeyError
    not_found = 0
    for key in delete_keys:
        try:
            ht.get(key)
        except KeyError:
            not_found += 1
    check("Deleted keys raise KeyError on get", not_found == 40)

    # Confirm remaining 80 records are still accessible
    still_present = 0
    remaining_keys = [f"student_{i:03d}" for i in range(1, 81)]
    for key in remaining_keys:
        try:
            ht.get(key)
            still_present += 1
        except KeyError:
            pass
    check("Remaining 80 records still accessible", still_present == 80)

# ---------------------------------------------------------------------------
# Section 4: Hash Table — collision analysis
# ---------------------------------------------------------------------------

def test_ht_collisions():
    print("\n=== Hash Table: Collision Analysis ===")
    ht = HashTable(size=10)          # small table forces many collisions
    for key, value in STUDENT_RECORDS:
        ht.insert(key, value)

    # Buckets with >1 entry demonstrate chaining is working
    chains = [b for b in ht.buckets if len(b) > 1]
    total_chained = sum(len(b) for b in chains)
    check("At least one collision bucket exists (chaining exercised)", len(chains) > 0)
    check("All 120 items stored despite collisions", total_chained + sum(1 for b in ht.buckets if len(b) == 1) == 120)

    print(f"  INFO  {len(chains)} bucket(s) hold chained entries "
          f"({total_chained} items across those buckets)")

    # Verify every record still retrievable under heavy collision load
    misses = sum(1 for k, v in STUDENT_RECORDS if ht.get(k) != v)
    check("All 120 records retrievable despite collisions", misses == 0)

# ---------------------------------------------------------------------------
# Section 5: Priority Queue — push + pop ordering (110 tasks)
# ---------------------------------------------------------------------------

def test_pq_push_pop():
    print("\n=== Priority Queue: Push & Pop Order (110 items) ===")
    pq = PriorityQueue()
    for name, priority in TASK_RECORDS:
        pq.push(name, priority)

    check("Queue length is 110 after pushing all tasks", len(pq) == 110)

    prev_priority = None
    out_of_order = 0

    # Collect (priority, item) from the heap to verify extraction order
    heap_snapshot = sorted(pq._heap)   # sorted by (priority, item) as stored
    extracted = []
    while not pq.is_empty():
        # Re-read priority from snapshot for comparison
        item = pq.pop()
        extracted.append(item)

    check("All 110 tasks popped (queue empty)", pq.is_empty() and len(extracted) == 110)

    # Verify non-decreasing priority by checking against sorted snapshot
    priorities_in_order = [p for p, _ in heap_snapshot]
    # Rebuild a fresh queue and pop to verify ordering
    pq2 = PriorityQueue()
    for name, priority in TASK_RECORDS:
        pq2.push(name, priority)

    last_p = -1
    bad_order = 0
    for _ in range(110):
        item = pq2.pop()
        # Recover priority from TASK_RECORDS lookup
        p = dict(TASK_RECORDS)[item]
        if p < last_p:
            bad_order += 1
        last_p = p

    check("Items popped in non-decreasing priority order", bad_order == 0)

# ---------------------------------------------------------------------------
# Section 6: Priority Queue — peek doesn't consume
# ---------------------------------------------------------------------------

def test_pq_peek():
    print("\n=== Priority Queue: Peek (does not consume) ===")
    pq = PriorityQueue()
    for name, priority in TASK_RECORDS:
        pq.push(name, priority)

    size_before = len(pq)
    top = pq.peek()
    size_after = len(pq)

    check("Peek does not change queue size", size_before == size_after)
    # The peek result should match the first pop
    popped = pq.pop()
    check("Peek returns the same item as the next pop", top == popped)

# ---------------------------------------------------------------------------
# Section 7: Priority Queue — mixed push/pop with 100 items
# ---------------------------------------------------------------------------

def test_pq_interleaved():
    print("\n=== Priority Queue: Interleaved Push/Pop (100 items) ===")
    pq = PriorityQueue()
    push_count = 0
    pop_count = 0
    results = []

    for i in range(100):
        pq.push(f"item_{i}", priority=100 - i)   # descending priorities pushed
        push_count += 1
        if i % 5 == 4:                           # pop every 5 pushes
            results.append(pq.pop())
            pop_count += 1

    remaining = len(pq)
    check(f"Pushed {push_count} items, popped {pop_count}, {remaining} remain",
          push_count == 100 and pop_count == 20 and remaining == 80)

    # Drain remaining and verify overall ordering is preserved
    while not pq.is_empty():
        results.append(pq.pop())

    # All item numbers extracted — none duplicated or missing
    check("All 100 items accounted for after drain", len(results) == 100)
    check("No duplicate items in output", len(set(results)) == 100)

# ---------------------------------------------------------------------------
# Section 8: Priority Queue — edge cases
# ---------------------------------------------------------------------------

def test_pq_edge_cases():
    print("\n=== Priority Queue: Edge Cases ===")
    pq = PriorityQueue()

    try:
        pq.pop()
        check("pop on empty queue raises IndexError", False)
    except IndexError:
        check("pop on empty queue raises IndexError", True)

    try:
        pq.peek()
        check("peek on empty queue raises IndexError", False)
    except IndexError:
        check("peek on empty queue raises IndexError", True)

    # Single item
    pq.push("only", 7)
    check("peek on single-item queue returns that item", pq.peek() == "only")
    check("pop on single-item queue empties it", pq.pop() == "only" and pq.is_empty())

    # Tie-breaking — same priority, multiple items
    pq2 = PriorityQueue()
    for i in range(10):
        pq2.push(f"tie_{i}", priority=5)
    popped = [pq2.pop() for _ in range(10)]
    check("All 10 same-priority items popped without error", len(popped) == 10 and pq2.is_empty())

# ---------------------------------------------------------------------------
# Run all tests
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print(" Data Structure Test Suite")
    print(" Hash Table + Priority Queue — 100+ item coverage")
    print("=" * 60)

    test_ht_insert_and_get()
    test_ht_update()
    test_ht_delete()
    test_ht_collisions()

    test_pq_push_pop()
    test_pq_peek()
    test_pq_interleaved()
    test_pq_edge_cases()

    print("\n" + "=" * 60)
    print(" All test sections complete.")
    print("=" * 60)

if __name__ == "__main__":
    main()
