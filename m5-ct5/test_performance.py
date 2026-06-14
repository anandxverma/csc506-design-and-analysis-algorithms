"""
Performance tests for HashTable and PriorityQueue using 100+ data items.
Compares hash table search vs. linear search on the same dataset.
"""

import time
import random
import string

from hash_table import HashTable
from priority_queue import PriorityQueue

# ── helpers ──────────────────────────────────────────────────────────────────

def random_string(length=6):
    """Return a random lowercase ASCII string of the given length."""
    return "".join(random.choices(string.ascii_lowercase, k=length))

def linear_search(pairs, target_key):
    """Scan `pairs` sequentially and return the value for `target_key`, or None if not found (O(n))."""
    for k, v in pairs:
        if k == target_key:
            return v
    return None

def timed(fn, *args, repeat=1_000):
    """Call fn(*args) `repeat` times and return the total wall-clock time in seconds."""
    start = time.perf_counter()
    for _ in range(repeat):
        fn(*args)
    return time.perf_counter() - start

# ── dataset ───────────────────────────────────────────────────────────────────

NUM_ITEMS = 120
random.seed(42)

keys   = [f"key_{random_string()}_{i}" for i in range(NUM_ITEMS)]
values = [random.randint(1, 10_000) for _ in range(NUM_ITEMS)]
pairs  = list(zip(keys, values))          # plain list for linear search

# ── 1. HashTable tests ────────────────────────────────────────────────────────

print("=" * 60)
print(f"  HashTable  —  {NUM_ITEMS} items, size=150")
print("=" * 60)

ht = HashTable(size=150)
for k, v in pairs:
    ht.insert(k, v)

# verify all items are retrievable
errors = 0
for k, v in pairs:
    try:
        assert ht.get(k) == v
    except (KeyError, AssertionError):
        errors += 1
print(f"  Insert + get verification : {'PASS' if errors == 0 else f'FAIL ({errors} errors)'}")

# spot-check 10 random keys
print("\n  Spot-check (10 random keys):")
sample = random.sample(pairs, 10)
for k, v in sample:
    result = ht.get(k)
    status = "OK" if result == v else "MISMATCH"
    print(f"    get({k!r}) -> {result}  [{status}]")

# update 20 keys
print("\n  Update 20 existing keys and re-verify:")
to_update = random.sample(pairs, 20)
for k, _ in to_update:
    ht.insert(k, 9999)
update_ok = all(ht.get(k) == 9999 for k, _ in to_update)
print(f"    Update verification : {'PASS' if update_ok else 'FAIL'}")

# delete 10 keys
print("\n  Delete 10 keys and confirm KeyError:")
to_delete = random.sample([k for k, _ in pairs], 10)
for k in to_delete:
    ht.delete(k)
delete_ok = True
for k in to_delete:
    try:
        ht.get(k)
        delete_ok = False
    except KeyError:
        pass
print(f"    Delete verification : {'PASS' if delete_ok else 'FAIL'}")

# bucket distribution
non_empty = sum(1 for b in ht.buckets if b)
total_chains = sum(len(b) for b in ht.buckets if len(b) > 1)
print(f"\n  Bucket stats  : {non_empty}/{ht.size} buckets used, "
      f"{total_chains} items in chains (collisions)")

# ── 1b. Collision demonstration ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("  Collision Demo  :  Engineered collisions on a small table")
print("=" * 60)

# The _hash() function sums ASCII values of all characters mod table size.
# Any anagram of a key produces an identical sum → guaranteed collision.
#   "abc" / "bca" / "cab" / "acb"  all have ASCII sum 294
#   "hello" / "lleho"              both have ASCII sum 532
COLL_SIZE = 8
ht_coll = HashTable(size=COLL_SIZE)

coll_pairs = [
    ("abc",   "alpha"),
    ("bca",   "bravo"),    # anagram of "abc" — guaranteed collision
    ("cab",   "charlie"),  # anagram of "abc" — guaranteed collision
    ("acb",   "delta"),    # anagram of "abc" — guaranteed collision
    ("hello", "echo"),
    ("lleho", "foxtrot"),  # anagram of "hello" — collides with "hello"
]

print(f"\n  Table size = {COLL_SIZE}   (hash = ASCII-sum mod {COLL_SIZE})\n")
print(f"  {'Key':<10} {'ASCII sum':>10} {'Bucket':>8}  Value")
print(f"  {'-'*10} {'-'*10} {'-'*8}  {'-'*10}")
for k, v in coll_pairs:
    ascii_sum = sum(ord(c) for c in k)
    idx = ascii_sum % COLL_SIZE
    ht_coll.insert(k, v)
    print(f"  {k:<10} {ascii_sum:>10} {idx:>8}  {v}")

print(f"\n  Bucket chains after all inserts:")
ht_coll.display_buckets()

hotspots = [(i, b) for i, b in enumerate(ht_coll.buckets) if len(b) > 1]
print(f"\n  {len(hotspots)} bucket(s) have chains (collisions):")
for i, b in hotspots:
    print(f"    bucket[{i}] has {len(b)} items  →  {len(b) - 1} collision(s)")

all_ok = all(ht_coll.get(k) == v for k, v in coll_pairs)
print(f"\n  All values reachable via chained get() : {'PASS' if all_ok else 'FAIL'}")

# ── performance impact: overloaded vs well-sized table ────────────────────────
print(f"\n  Performance impact  :  overloaded table (size=10) vs well-sized (size=150)")
print(f"  Same {NUM_ITEMS} keys inserted into both\n")

ht_small = HashTable(size=10)
ht_large = HashTable(size=150)
for k, v in pairs:
    ht_small.insert(k, v)
    ht_large.insert(k, v)

max_chain_small = max(len(b) for b in ht_small.buckets)
max_chain_large = max(len(b) for b in ht_large.buckets)
used_small = sum(1 for b in ht_small.buckets if b)
used_large = sum(1 for b in ht_large.buckets if b)
avg_chain_small = NUM_ITEMS / used_small
avg_chain_large = NUM_ITEMS / used_large

print(f"  {'Table':<14} {'Size':>6}  {'Buckets used':>13}  {'Max chain':>10}  {'Avg chain':>10}")
print(f"  {'-'*14} {'-'*6}  {'-'*13}  {'-'*10}  {'-'*10}")
print(f"  {'Overloaded':<14} {10:>6}  {used_small:>13}  {max_chain_small:>10}  {avg_chain_small:>10.1f}")
print(f"  {'Well-sized':<14} {150:>6}  {used_large:>13}  {max_chain_large:>10}  {avg_chain_large:>10.1f}")

REPEAT_COLL = 500
target_coll = keys[NUM_ITEMS // 2]
t_small_coll = timed(ht_small.get, target_coll, repeat=REPEAT_COLL) * 1000
t_large_coll = timed(ht_large.get, target_coll, repeat=REPEAT_COLL) * 1000
slowdown = t_small_coll / t_large_coll if t_large_coll > 0 else float("inf")
print(f"\n  get({target_coll!r}) × {REPEAT_COLL:,} repetitions:")
print(f"    Overloaded (size=10)  : {t_small_coll:.2f} ms")
print(f"    Well-sized (size=150) : {t_large_coll:.2f} ms")
print(f"    Slowdown from collision chains : {slowdown:.1f}x")

# ── 2. Search performance comparison ─────────────────────────────────────────

print("\n" + "=" * 60)
print("  Search Performance  :  Hash Table vs. Linear Search")
print("=" * 60)

# rebuild ht with all original values for a fair comparison
ht2 = HashTable(size=150)
for k, v in pairs:
    ht2.insert(k, v)

REPEAT = 500

# test against keys at different positions in the list
positions = {
    "first item":  keys[0],
    "middle item": keys[NUM_ITEMS // 2],
    "last item":   keys[-1],
}

print(f"\n  Searches repeated {REPEAT:,} times each\n")
print(f"  {'Target':<15} {'Hash (ms)':>12} {'Linear (ms)':>14} {'Speedup':>10}")
print(f"  {'-'*15} {'-'*12} {'-'*14} {'-'*10}")

for label, target_key in positions.items():
    t_hash   = timed(ht2.get, target_key,           repeat=REPEAT) * 1000
    t_linear = timed(linear_search, pairs, target_key, repeat=REPEAT) * 1000
    speedup  = t_linear / t_hash if t_hash > 0 else float("inf")
    print(f"  {label:<15} {t_hash:>11.2f}  {t_linear:>13.2f}  {speedup:>9.1f}x")

# aggregate over all 120 keys
REPEAT_ALL = 100
print(f"\n  {'All 120 keys':<15} (total time for {REPEAT_ALL:,} full scans each)")
t_hash_all   = timed(lambda: [ht2.get(k) for k, _ in pairs], repeat=REPEAT_ALL) * 1000
t_linear_all = timed(lambda: [linear_search(pairs, k) for k, _ in pairs], repeat=REPEAT_ALL) * 1000
speedup_all  = t_linear_all / t_hash_all if t_hash_all > 0 else float("inf")
print(f"  {'Hash total':<15} {t_hash_all:>11.2f} ms")
print(f"  {'Linear total':<15} {t_linear_all:>11.2f} ms")
print(f"  {'Speedup':<15} {speedup_all:>11.1f}x")

# ── 3. PriorityQueue tests ────────────────────────────────────────────────────

print("\n" + "=" * 60)
print(f"  PriorityQueue  —  {NUM_ITEMS} items")
print("=" * 60)

pq = PriorityQueue()
priorities = [random.randint(1, 1000) for _ in range(NUM_ITEMS)]
items      = [f"task_{i}" for i in range(NUM_ITEMS)]

for item, pri in zip(items, priorities):
    pq.push(item, pri)

print(f"  Pushed {NUM_ITEMS} items. Size: {len(pq)}")
print(f"  Peek (min priority): {pq.peek()}")

# rebuild with (priority, item) tracking to verify pop order
pq2 = PriorityQueue()
for item, pri in zip(items, priorities):
    pq2.push((pri, item), pri)

popped = []
while not pq2.is_empty():
    entry = pq2.pop()
    popped.append(entry[0])  # collect priority

is_sorted = all(popped[i] <= popped[i + 1] for i in range(len(popped) - 1))
print(f"  Pop order ascending : {'PASS' if is_sorted else 'FAIL'}")
print(f"  First 10 priorities : {popped[:10]}")
print(f"  Last  10 priorities : {popped[-10:]}")

# push/pop performance
pq3 = PriorityQueue()
t_push = timed(lambda: pq3.push("x", random.randint(1, 1000)), repeat=NUM_ITEMS) * 1000
print(f"\n  Push {NUM_ITEMS} items     : {t_push:.3f} ms")
t_pop = timed(pq3.pop, repeat=min(len(pq3), NUM_ITEMS)) * 1000
print(f"  Pop  {NUM_ITEMS} items     : {t_pop:.3f} ms")

print("\n" + "=" * 60)
print("  All tests complete.")
print("=" * 60)
