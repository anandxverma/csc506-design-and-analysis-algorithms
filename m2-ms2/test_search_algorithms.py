import random
from search_algorithms import binary_search, linear_search, time_search

RUNS = 5
sizes = [100, 1000, 10000]

print(f"{'Size':<10} {'Algorithm':<16} {'Target':<8} {'Result':<10} {'Avg (ms)':<14} {'Min (ms)':<14} {'Max (ms)'}")
print("-" * 80)

for size in sizes:
    arr = sorted(random.sample(range(size * 10), size))
    target_hit = random.choice(arr)
    target_miss = -1

    for target, label in [(target_hit, "hit"), (target_miss, "miss")]:
        for name, fn in [("binary_search", binary_search), ("linear_search", linear_search)]:
            result, avg, lo, hi = time_search(fn, arr, target, runs=RUNS)
            print(f"{size:<10} {name:<16} {label:<8} {result:<10} {avg:<14.6f} {lo:<14.6f} {hi:.6f}")
