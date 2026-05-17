"""
benchmark.py — measure actual runtimes for Stack / Queue / LinkedList operations
at increasing input sizes, then fit predicted O(1) and O(n) curves to the data.

Returns structured BenchmarkResult objects consumed by the GUI's PerfTab.
"""

import time
import statistics
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from stack import Stack
from queue import Queue
from linked_list import LinkedList

# Input sizes to test (number of pre-loaded elements before each timed op)
SIZES = [100, 500, 1_000, 2_500, 5_000, 10_000, 25_000, 50_000]
REPEATS = 7   # median over this many repetitions per (size, op) pair


# ── result container ──────────────────────────────────────────────────────────

class OperationResult:
    __slots__ = ("name", "complexity", "sizes", "times_us", "predicted_us")

    def __init__(self, name: str, complexity: str,
                 sizes: list[int], times_us: list[float], predicted_us: list[float]):
        self.name         = name
        self.complexity   = complexity   # "O(1)" or "O(n)"
        self.sizes        = sizes
        self.times_us     = times_us     # measured median times in microseconds
        self.predicted_us = predicted_us # fitted curve in microseconds


class DSResult:
    __slots__ = ("ds_name", "operations")

    def __init__(self, ds_name: str, operations: list[OperationResult]):
        self.ds_name    = ds_name
        self.operations = operations


# ── timing helper ─────────────────────────────────────────────────────────────

def _median_us(fn, repeats: int) -> float:
    """Return median elapsed time in microseconds over `repeats` calls."""
    samples = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - t0) * 1_000_000)
    return statistics.median(samples)


# ── curve fitting ─────────────────────────────────────────────────────────────

def _fit_predicted(complexity: str, sizes: list[int], times_us: list[float]) -> list[float]:
    """
    Fit a predicted curve to the measured data.

    O(1)  → constant: mean of measured times (flat line)
    O(n)  → linear:   least-squares fit  t = a·n + b  (numpy-free, pure Python)
    """
    n = len(sizes)
    if complexity == "O(1)":
        c = sum(times_us) / n
        return [c] * n

    # simple linear least-squares: t = a·x + b
    sx  = sum(sizes)
    sy  = sum(times_us)
    sxx = sum(x * x for x in sizes)
    sxy = sum(x * y for x, y in zip(sizes, times_us))
    denom = n * sxx - sx * sx
    if denom == 0:
        return times_us[:]
    a = (n * sxy - sx * sy) / denom
    b = (sy - a * sx) / n
    return [a * x + b for x in sizes]


# ── per-structure benchmarks ──────────────────────────────────────────────────

def _bench_stack() -> DSResult:
    ops: list[OperationResult] = []

    # Push — O(1)
    push_times = []
    for n in SIZES:
        s = Stack()
        for i in range(n):
            s.push(i)
        push_times.append(_median_us(lambda s=s: s.push(999), REPEATS))
    ops.append(OperationResult("Push", "O(1)", SIZES[:], push_times,
                               _fit_predicted("O(1)", SIZES, push_times)))

    # Pop — O(1)
    pop_times = []
    for n in SIZES:
        s = Stack()
        for i in range(n + REPEATS + 1):
            s.push(i)
        pop_times.append(_median_us(lambda s=s: s.pop(), REPEATS))
    ops.append(OperationResult("Pop", "O(1)", SIZES[:], pop_times,
                               _fit_predicted("O(1)", SIZES, pop_times)))

    # Search — O(n): search for a value that doesn't exist (worst case)
    search_times = []
    for n in SIZES:
        s = Stack()
        for i in range(n):
            s.push(i)
        search_times.append(_median_us(
            lambda s=s: (lambda: [x for x in s._items if x == -1])(),
            REPEATS))
    ops.append(OperationResult("Search", "O(n)", SIZES[:], search_times,
                               _fit_predicted("O(n)", SIZES, search_times)))

    return DSResult("Stack", ops)


def _bench_queue() -> DSResult:
    ops: list[OperationResult] = []

    # Enqueue — O(1)
    enq_times = []
    for n in SIZES:
        q = Queue()
        for i in range(n):
            q.enqueue(i)
        enq_times.append(_median_us(lambda q=q: q.enqueue(999), REPEATS))
    ops.append(OperationResult("Enqueue", "O(1)", SIZES[:], enq_times,
                               _fit_predicted("O(1)", SIZES, enq_times)))

    # Dequeue — O(1)
    deq_times = []
    for n in SIZES:
        q = Queue()
        for i in range(n + REPEATS + 1):
            q.enqueue(i)
        deq_times.append(_median_us(lambda q=q: q.dequeue(), REPEATS))
    ops.append(OperationResult("Dequeue", "O(1)", SIZES[:], deq_times,
                               _fit_predicted("O(1)", SIZES, deq_times)))

    # Search — O(n): scan for absent value
    search_times = []
    for n in SIZES:
        q = Queue()
        for i in range(n):
            q.enqueue(i)
        search_times.append(_median_us(
            lambda q=q: (lambda: [x for x in q._items if x == -1])(),
            REPEATS))
    ops.append(OperationResult("Search", "O(n)", SIZES[:], search_times,
                               _fit_predicted("O(n)", SIZES, search_times)))

    return DSResult("Queue", ops)


def _bench_linked_list() -> DSResult:
    ops: list[OperationResult] = []

    # Prepend — O(1)
    pre_times = []
    for n in SIZES:
        ll = LinkedList()
        for i in range(n):
            ll.append(i)
        pre_times.append(_median_us(lambda ll=ll: ll.prepend(999), REPEATS))
    ops.append(OperationResult("Prepend", "O(1)", SIZES[:], pre_times,
                               _fit_predicted("O(1)", SIZES, pre_times)))

    # Append — O(n): must walk to tail each time
    app_times = []
    for n in SIZES:
        ll = LinkedList()
        for i in range(n):
            ll.append(i)
        app_times.append(_median_us(lambda ll=ll: ll.append(999), REPEATS))
    ops.append(OperationResult("Append", "O(n)", SIZES[:], app_times,
                               _fit_predicted("O(n)", SIZES, app_times)))

    # Search hit — O(n) worst: search for last element
    search_times = []
    for n in SIZES:
        ll = LinkedList()
        for i in range(n):
            ll.append(i)
        target = str(n - 1) if ll.search(str(n - 1)) else n - 1
        search_times.append(_median_us(lambda ll=ll, t=n-1: ll.search(t), REPEATS))
    ops.append(OperationResult("Search", "O(n)", SIZES[:], search_times,
                               _fit_predicted("O(n)", SIZES, search_times)))

    # Delete tail — O(n) worst case
    del_times = []
    for n in SIZES:
        ll = LinkedList()
        for i in range(n):
            ll.append(i)
        # Re-insert tail before each timed deletion so size stays ~n
        def _del_tail(ll=ll, n=n):
            ll.append(n)
            ll.delete(n)
        del_times.append(_median_us(_del_tail, REPEATS))
    ops.append(OperationResult("Delete (tail)", "O(n)", SIZES[:], del_times,
                               _fit_predicted("O(n)", SIZES, del_times)))

    return DSResult("Linked List", ops)


# ── public entry point ────────────────────────────────────────────────────────

def run_all(progress_cb=None) -> list[DSResult]:
    """
    Run all benchmarks.  Optional `progress_cb(pct: int, label: str)` is called
    with 0-100 progress so the GUI can update a progress bar.
    """
    steps = [
        ("Stack",       _bench_stack),
        ("Queue",       _bench_queue),
        ("Linked List", _bench_linked_list),
    ]
    results = []
    for i, (label, fn) in enumerate(steps):
        if progress_cb:
            progress_cb(int(i / len(steps) * 100), f"Benchmarking {label}…")
        results.append(fn())
    if progress_cb:
        progress_cb(100, "Done")
    return results


# ── CLI quick-check ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    def _cb(pct, label):
        print(f"[{pct:3d}%] {label}")

    for ds in run_all(_cb):
        print(f"\n{'─'*55}")
        print(f"  {ds.ds_name}")
        print(f"{'─'*55}")
        for op in ds.operations:
            measured = ", ".join(f"{t:.2f}" for t in op.times_us)
            print(f"  {op.name:<20} {op.complexity}  measured(µs): {measured}")
