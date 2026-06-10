# Algorithms that leverage the Deque data structure.
# Each algorithm demonstrates a distinct capability of the double-ended queue.
#
# Algorithm 1 – Palindrome Checker      O(n) time / O(n) space
# Algorithm 2 – Sliding-Window Maximum  O(n) time / O(k) space
# Algorithm 3 – BFS Shortest Path       O(V+E) time / O(V) space

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from deque import Deque


# ---------------------------------------------------------------------------
# Algorithm 1 – Palindrome Checker
#
# Load every character into the deque, then peel one character off each end
# and compare.  A mismatch immediately proves it is not a palindrome.
# All characters are lowercased before comparison.
# ---------------------------------------------------------------------------

def is_palindrome(s: str) -> bool:
    """Return True if s is a palindrome (case-insensitive)."""
    d = Deque()
    for ch in s.lower():
        d.addRear(ch)

    while d.size() > 1:
        if d.removeFront() != d.removeRear():
            return False
    return True


# ---------------------------------------------------------------------------
# Algorithm 2 – Sliding-Window Maximum (monotonic deque)
#
# Keep a deque of *indices* into nums such that the values at those indices
# are in strictly decreasing order.
#   - Front  → index of the current window's maximum value.
#   - Rear   → most recently added candidate index.
#
# Before adding index i:
#   1. Evict the front if it has slid out of the window (index <= i - k).
#   2. Evict the rear while the value there is <= nums[i]; those indices can
#      never be the window max while i is still in the window.
# ---------------------------------------------------------------------------

def sliding_window_max(nums: list, k: int) -> list:
    """Return the maximum value for each sliding window of width k."""
    if not nums or k <= 0:
        return []

    index_deque = Deque()   # stores indices into nums
    result = []

    for i, val in enumerate(nums):
        # Remove front index if it has left the window
        if not index_deque.isEmpty() and index_deque._items[0] <= i - k:
            index_deque.removeFront()

        # Maintain decreasing order from front to rear
        while not index_deque.isEmpty() and nums[index_deque._items[-1]] <= val:
            index_deque.removeRear()

        index_deque.addRear(i)

        if i >= k - 1:
            result.append(nums[index_deque._items[0]])

    return result


# ---------------------------------------------------------------------------
# Algorithm 3 – BFS Shortest Path on an Unweighted Grid
#
# Use the deque as a FIFO queue (addRear to enqueue, removeFront to dequeue).
# BFS guarantees the first time a cell is reached it is via the shortest path.
# A parent map records how each cell was reached, enabling path reconstruction.
#
# grid: 2-D list where 0 = open cell, 1 = wall
# ---------------------------------------------------------------------------

def bfs_shortest_path(grid: list, start: tuple, end: tuple) -> list:
    """
    Return the shortest path from start to end as a list of (row, col) tuples.
    Returns an empty list if no path exists.
    """
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    parent = {}

    queue = Deque()
    queue.addRear(start)
    visited[start[0]][start[1]] = True

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while not queue.isEmpty():
        cell = queue.removeFront()

        if cell == end:
            path = []
            while cell in parent:
                path.append(cell)
                cell = parent[cell]
            path.append(start)
            path.reverse()
            return path

        r, c = cell
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and not visited[nr][nc]
                    and grid[nr][nc] == 0):
                visited[nr][nc] = True
                parent[(nr, nc)] = cell
                queue.addRear((nr, nc))

    return []


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # --- Algorithm 1: Palindrome Checker ---
    print("=== Algorithm 1: Palindrome Checker ===")
    print("  Used to determine if a given word is a palindrome.")
    print()
    test_words = ["racecar", "hello", "level", "world", "madam", "python"]
    for word in test_words:
        result = is_palindrome(word)
        print(f"  is_palindrome({word!r:<10}) -> {result}")

    # --- Algorithm 2: Sliding-Window Maximum ---
    print("\n=== Algorithm 2: Sliding-Window Maximum ===")
    print("  Used to find the maximum value within each fixed-size sliding window of a list.")
    print()
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    maxes = sliding_window_max(nums, k)
    print(f"  nums            = {nums}")
    print(f"  window size k   = {k}")
    print(f"  window maximums = {maxes}")

    # --- Algorithm 3: BFS Shortest Path ---
    print("\n=== Algorithm 3: BFS Shortest Path on Grid ===")
    print("  Used to find the shortest path between two cells on an unweighted grid.")
    print()
    grid = [
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    start, end = (0, 0), (4, 4)
    path = bfs_shortest_path(grid, start, end)

    print("  Grid (0=open, 1=wall):")
    for row in grid:
        print(f"    {row}")
    print(f"  Start : {start}")
    print(f"  End   : {end}")
    if path:
        print(f"  Path  : {path}  ({len(path)} cells)")
    else:
        print("  No path found.")
