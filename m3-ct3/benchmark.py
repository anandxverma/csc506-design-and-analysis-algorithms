# Sorting Algorithm Benchmark + Analysis
#
# Runs every (algorithm × dataset × size) combination, prints a live results
# table, then follows up with three analysis sections:
#   1. Best Algorithm per Scenario — fastest algorithm for each (dataset, size)
#      pair with the winner time and gap to the runner-up.
#   2. Algorithm Win Summary — how many scenarios each algorithm won.
#   3. When to Use Each Algorithm — plain-English recommendation guide.
#
# O(n^2) algorithms (bubble, selection, insertion) are skipped at n=50000 by
# default because they would take several minutes.  Change SKIP_SLOW_AT to
# None to disable that guard or to a different threshold.

import copy
import csv
import os
import sys
import time
from collections import defaultdict

from bubble_sort import bubble_sort
from data_generator import GENERATORS, generate
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from selection_sort import selection_sort

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SIZES = [1000, 5000, 10000, 50000]

DATASET_TYPES = list(GENERATORS.keys())

ALGORITHMS = [
    ("Bubble Sort",    bubble_sort),
    ("Insertion Sort", insertion_sort),
    ("Selection Sort", selection_sort),
    ("Merge Sort",     merge_sort),
]

SKIP_SLOW_AT = 50_000
SLOW_ALGORITHMS = {"Bubble Sort", "Insertion Sort", "Selection Sort"}

# ---------------------------------------------------------------------------
# Benchmark table formatting
# ---------------------------------------------------------------------------

_COL_ALGO    = 16
_COL_DATASET = 18
_COL_SIZE    = 8
_COL_TIME    = 12
_COL_STATUS  = 8

_BENCH_WIDTH = _COL_ALGO + _COL_DATASET + _COL_SIZE + _COL_TIME + 2 + _COL_STATUS


def _bench_header():
    return (
        f"{'Algorithm':<{_COL_ALGO}}"
        f"{'Dataset':<{_COL_DATASET}}"
        f"{'Size':>{_COL_SIZE}}"
        f"{'Time (s)':>{_COL_TIME}}"
        f"  {'Status':<{_COL_STATUS}}"
    )


def _bench_separator():
    return "-" * _BENCH_WIDTH


def _bench_row(algo_name, dataset_type, size, elapsed, correct):
    status = "OK" if correct else "FAIL"
    return (
        f"{algo_name:<{_COL_ALGO}}"
        f"{dataset_type:<{_COL_DATASET}}"
        f"{size:>{_COL_SIZE}}"
        f"{elapsed:>{_COL_TIME}.6f}"
        f"  {status:<{_COL_STATUS}}"
    )


# ---------------------------------------------------------------------------
# Analysis report formatting
# ---------------------------------------------------------------------------

_W_DATASET = 18
_W_SIZE    = 8
_W_WINNER  = 16
_W_TIME    = 12
_W_GAP     = 14
_W_RUNNERS = 36

_RPT_WIDTH = _W_DATASET + _W_SIZE + _W_WINNER + _W_TIME + _W_GAP + _W_RUNNERS


def _rpt_divider():
    return "-" * _RPT_WIDTH


def _rpt_section(title):
    return f"\n{'=' * _RPT_WIDTH}\n  {title}\n{'=' * _RPT_WIDTH}"


# ---------------------------------------------------------------------------
# Benchmark run (prints table + collects results for analysis)
# ---------------------------------------------------------------------------

def run_benchmark():
    """Run every (algorithm × dataset × size) combination.

    Prints the benchmark results table to stdout and returns a dict mapping
    (dataset_type, size) -> list of (algo_name, elapsed) for use by the
    analysis sections below.
    """
    print("\nSorting Algorithm Benchmark")
    print("=" * _BENCH_WIDTH)
    print(_bench_header())
    print(_bench_separator())

    results = defaultdict(list)
    failures = []
    raw_rows = []

    for algo_name, algo_fn in ALGORITHMS:
        for dataset_type in DATASET_TYPES:
            for size in SIZES:

                if SKIP_SLOW_AT and algo_name in SLOW_ALGORITHMS and size >= SKIP_SLOW_AT:
                    skipped_row = (
                        f"{algo_name:<{_COL_ALGO}}"
                        f"{dataset_type:<{_COL_DATASET}}"
                        f"{size:>{_COL_SIZE}}"
                        f"{'(skipped)':>{_COL_TIME}}"
                        f"  {'--':<{_COL_STATUS}}"
                    )
                    print(skipped_row)
                    raw_rows.append((algo_name, dataset_type, size, None, "skipped"))
                    continue

                data = generate(dataset_type, size)
                data_copy = copy.copy(data)

                start = time.perf_counter()
                result = algo_fn(data_copy)
                elapsed = time.perf_counter() - start

                expected = sorted(data)
                correct = result == expected

                if not correct:
                    failures.append((algo_name, dataset_type, size))

                results[(dataset_type, size)].append((algo_name, elapsed))
                raw_rows.append((algo_name, dataset_type, size, elapsed, "OK" if correct else "FAIL"))
                print(_bench_row(algo_name, dataset_type, size, elapsed, correct))

        print()

    print(_bench_separator())
    if failures:
        print(f"\nFAILURES ({len(failures)}):")
        for algo_name, dataset_type, size in failures:
            print(f"  {algo_name} | {dataset_type} | n={size}")
        sys.exit(1)
    else:
        print("\nAll tests passed.")

    return results, raw_rows


# ---------------------------------------------------------------------------
# Analysis sections
# ---------------------------------------------------------------------------

def print_best_per_scenario(results):
    """Print the fastest algorithm for every (dataset, size) pair."""

    print(_rpt_section("Best Algorithm per Scenario"))
    print(
        f"{'Dataset':<{_W_DATASET}}"
        f"{'Size':>{_W_SIZE}}"
        f"  {'Winner':<{_W_WINNER}}"
        f"{'Time (s)':>{_W_TIME}}"
        f"{'vs 2nd (x)':>{_W_GAP}}"
        f"  Runners-up"
    )
    print(_rpt_divider())

    prev_dataset = None

    for dataset_type in DATASET_TYPES:
        for size in SIZES:
            key = (dataset_type, size)
            if key not in results:
                continue

            entries = sorted(results[key], key=lambda x: x[1])

            if not entries:
                continue

            winner_name, winner_time = entries[0]

            if len(entries) >= 2:
                second_time = entries[1][1]
                gap = second_time / winner_time if winner_time > 0 else float("inf")
                gap_str = f"{gap:.2f}x"
            else:
                gap_str = "N/A"

            runners = ", ".join(f"{name} ({t:.4f}s)" for name, t in entries[1:])

            if prev_dataset and prev_dataset != dataset_type:
                print()
            prev_dataset = dataset_type

            print(
                f"{dataset_type:<{_W_DATASET}}"
                f"{size:>{_W_SIZE}}"
                f"  {winner_name:<{_W_WINNER}}"
                f"{winner_time:>{_W_TIME}.6f}"
                f"{gap_str:>{_W_GAP}}"
                f"  {runners}"
            )

    print(_rpt_divider())


def print_win_summary(results):
    """Print how many scenarios each algorithm won."""

    win_counts = defaultdict(int)
    total_scenarios = 0

    for entries in results.values():
        if not entries:
            continue
        best_name = min(entries, key=lambda x: x[1])[0]
        win_counts[best_name] += 1
        total_scenarios += 1

    print(_rpt_section("Algorithm Win Summary"))
    print(f"  {'Algorithm':<{_W_WINNER}}  {'Wins':>6}  {'Win %':>8}")
    print(_rpt_divider())

    for algo_name, _ in sorted(ALGORITHMS, key=lambda a: win_counts[a[0]], reverse=True):
        wins = win_counts[algo_name]
        pct = 100 * wins / total_scenarios if total_scenarios else 0
        print(f"  {algo_name:<{_W_WINNER}}  {wins:>6}  {pct:>7.1f}%")

    print(_rpt_divider())
    print(f"  Total scenarios evaluated: {total_scenarios}")
    print()


def print_scenario_recommendation():
    """Print a plain-English recommendation guide."""

    print(_rpt_section("When to Use Each Algorithm"))
    recommendations = [
        ("Merge Sort",
         "Best general-purpose choice. O(n log n) guaranteed across all inputs. "
         "Use by default, especially for large or unknown data."),
        ("Insertion Sort",
         "Fastest O(n^2) algorithm on small or nearly-sorted data. "
         "Practical threshold: n < ~1000 or partially_sorted inputs."),
        ("Bubble Sort",
         "Rarely preferred; use only as a teaching example. "
         "Adaptive variant is competitive on sorted input, but insertion sort is better."),
        ("Selection Sort",
         "Consistent O(n^2) regardless of input order. "
         "Useful when the cost of writes (swaps) dominates reads; O(n) swaps."),
    ]

    for name, note in recommendations:
        print(f"\n  {name}")
        words = note.split()
        line, lines = [], []
        for w in words:
            if sum(len(x) + 1 for x in line) + len(w) > 72:
                lines.append(" ".join(line))
                line = []
            line.append(w)
        if line:
            lines.append(" ".join(line))
        for l in lines:
            print(f"    {l}")

    print(f"\n{'=' * _RPT_WIDTH}\n")


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------

def export_csv(raw_rows):
    """Prompt the user for a file path and write the benchmark rows to CSV."""
    answer = input("Export benchmark results to CSV? [y/N]: ").strip().lower()
    if answer not in ("y", "yes"):
        print("Skipping CSV export.")
        return

    default_path = os.path.join(os.getcwd(), "benchmark_results.csv")
    prompt = f"File path [{default_path}]: "
    path = input(prompt).strip()
    if not path:
        path = default_path

    path = os.path.expanduser(path)
    dir_name = os.path.dirname(path)
    if dir_name and not os.path.isdir(dir_name):
        print(f"Directory does not exist: {dir_name}")
        return

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algorithm", "Dataset", "Size", "Time (s)", "Status"])
        for algo_name, dataset_type, size, elapsed, status in raw_rows:
            writer.writerow([
                algo_name,
                dataset_type,
                size,
                f"{elapsed:.6f}" if elapsed is not None else "",
                status,
            ])

    print(f"Results exported to {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    results, raw_rows = run_benchmark()
    print_best_per_scenario(results)
    print_win_summary(results)
    print_scenario_recommendation()
    export_csv(raw_rows)
