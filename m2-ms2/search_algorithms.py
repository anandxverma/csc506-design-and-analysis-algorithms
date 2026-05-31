import time


def time_search(fn, arr, target, runs=1):
    """Run fn(arr, target) `runs` times and return (result, avg_ms, min_ms, max_ms)."""
    times = []
    result = None
    for _ in range(runs):
        start = time.perf_counter()
        result = fn(arr, target)
        times.append((time.perf_counter() - start) * 1_000)
    avg = sum(times) / len(times)
    return result, avg, min(times), max(times)


def binary_search(arr, target):
    """Returns the index of target in a sorted arr, or -1 if not found."""
    # Start with the full range of the array
    low, high = 0, len(arr) - 1

    while low <= high:
        # Find the middle index of the current search range
        mid = (low + high) // 2

        if arr[mid] == target:
            # Found the target at the midpoint
            return mid
        elif arr[mid] < target:
            # Target is in the right half; discard the left
            low = mid + 1
        else:
            # Target is in the left half; discard the right
            high = mid - 1

    # Target was not found in the array
    return -1


def linear_search(arr, target):
    """Returns the index of target in arr, or -1 if not found."""
    # Check each element one by one from left to right
    for i, val in enumerate(arr):
        if val == target:
            # Return the index as soon as a match is found
            return i

    # Target was not found in the array
    return -1
