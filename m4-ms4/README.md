# CSC 506 – Module 4 Milestone: Linear Data Structures & Algorithm Analysis

A Python implementation of four fundamental linear data structures — **Stack**, **Queue**, **Deque**, and **Linked List** — along with classic algorithms built on each, and a scenario analysis comparing all four structures against real-world problems.

---

## Project Structure

```
m4-ms4/
├── stack.py              # LIFO Stack
├── queue.py              # FIFO Queue
├── deque.py              # Double-Ended Queue
├── linked_list.py        # Singly Linked List
├── scenario_analysis.py  # Four real-world scenarios comparing all structures
└── algorithms/
    ├── algorithms_stack.py        # Bracket validator, infix→postfix, DFS
    ├── algorithms_queue.py        # BFS, level-order traversal, round-robin scheduler
    ├── algorithms_deque.py        # Palindrome checker, sliding-window max, BFS on grid
    └── algorithms_linked_list.py  # Cycle detection, in-place reversal, merge sorted lists
```

---

## Data Structures

### Stack (`stack.py`)
Last-in, first-out (LIFO) structure backed by a Python list.

| Operation | Time Complexity |
|-----------|----------------|
| `push(item)` | O(1) amortized |
| `pop()` | O(1) |
| `peek()` | O(1) |
| `is_empty()` / `size()` | O(1) |

### Queue (`queue.py`)
First-in, first-out (FIFO) structure backed by a Python list.

| Operation | Time Complexity |
|-----------|----------------|
| `enqueue(item)` | O(1) amortized |
| `dequeue()` | O(n) — list shift at index 0 |
| `front()` | O(1) |
| `is_empty()` / `size()` | O(1) |

> Note: `dequeue` is O(n) due to the list-backed implementation. Use `collections.deque` for O(1) in production.

### Deque (`deque.py`)
Double-ended queue supporting O(1) operations at the rear and O(n) at the front (due to list shifting).

| Operation | Time Complexity |
|-----------|----------------|
| `addRear(item)` | O(1) amortized |
| `removeRear()` | O(1) |
| `addFront(item)` | O(n) |
| `removeFront()` | O(n) |
| `isEmpty()` / `size()` | O(1) |

### Linked List (`linked_list.py`)
Singly linked list with head pointer and size tracking.

| Operation | Time Complexity |
|-----------|----------------|
| `insert(data, index)` | O(n) |
| `delete(data)` | O(n) |
| `search(data)` | O(n) |
| `display()` | O(n) |
| `is_empty()` / `size()` | O(1) |

---

## Algorithms

### Stack Algorithms (`algorithms/algorithms_stack.py`)

**1. Balanced Bracket Validator** — O(n) time / O(n) space
Validates that every opening bracket `(`, `[`, `{` in an expression is closed in the correct order. The LIFO property enforces nesting: the most recently opened bracket must be the next one closed.

**2. Infix to Postfix (Shunting-Yard) + Evaluator** — O(n) time / O(n) space
Converts a human-readable infix expression (e.g. `3 + 4 * 2`) to Reverse Polish Notation using an operator stack to enforce precedence and associativity, then evaluates the postfix form with a second stack pass.

**3. Iterative Depth-First Search (DFS)** — O(V + E) time / O(V) space
Explores a graph using an explicit LIFO stack instead of recursion, diving as deep as possible before backtracking. Avoids Python's recursion limit on large graphs.

---

### Queue Algorithms (`algorithms/algorithms_queue.py`)

**1. Breadth-First Search (BFS)** — O(V + E) time / O(V) space
Explores a graph level by level from a source vertex. The FIFO queue guarantees that vertices discovered earlier are visited earlier, producing the shortest-hop traversal and shortest path in unweighted graphs.

**2. Level-Order Binary Tree Traversal** — O(n) time / O(W) space
Visits every node in a binary tree row by row. Snapshotting the queue size before each batch isolates individual levels without needing explicit depth tracking.

**3. Round-Robin CPU Scheduler** — O(n × ceil(burst_max / quantum)) time
Simulates a preemptive CPU scheduler where each process receives a fixed time quantum. Processes that don't finish are re-enqueued at the tail, giving every process a fair, equal turn.

---

### Deque Algorithms (`algorithms/algorithms_deque.py`)

**1. Palindrome Checker** — O(n) time / O(n) space
Loads all characters into the deque, then peels one character from each end and compares. A mismatch immediately proves it is not a palindrome.

**2. Sliding-Window Maximum** — O(n) time / O(k) space
Maintains a monotonic deque of indices such that values are in strictly decreasing order. The front always holds the current window's maximum index; stale or dominated indices are evicted from the appropriate end.

**3. BFS Shortest Path on a Grid** — O(V + E) time / O(V) space
Uses the deque as a FIFO queue (addRear/removeFront) to find the shortest path between two cells on a 2D grid with walls.

---

### Linked List Algorithms (`algorithms/algorithms_linked_list.py`)

**1. Floyd's Cycle Detection (Tortoise and Hare)** — O(n) time / O(1) space
A slow pointer advances one node per step and a fast pointer advances two. If a cycle exists they meet inside the loop. A second phase finds the exact entry node of the cycle.

**2. In-Place Reversal** — O(n) time / O(1) space
Three pointers (`prev`, `current`, `nxt`) traverse the list once, re-wiring each node's next pointer to point backward. No extra nodes or array copies are needed.

**3. Merge Two Sorted Linked Lists** — O(n + m) time / O(1) space
A dummy sentinel node anchors the result. At each step the smaller of the two current nodes is appended by re-linking its next pointer — zero new node allocations.

---

## Scenario Analysis (`scenario_analysis.py`)

Each scenario is implemented with all four data structures so the trade-offs are concrete and observable. Output explains the best fit and why the others are less efficient.

| Scenario | Best Fit | Core Access Pattern |
|---|---|---|
| Browser Back Button | **Stack** | LIFO — always undo the most recent |
| Printer Queue | **Queue** | FIFO — first submitted, first printed |
| Browser History with Recycling | **Deque** | Both-ends — cap oldest, scroll newest |
| Song Playlist | **Linked List** | Mid-list insert/delete via pointer rewire |

---

## Running the Code

Each file can be run directly as a standalone script:

```bash
# Data structure demos
python stack.py
python queue.py
python deque.py
python linked_list.py

# Algorithm demos
python algorithms/algorithms_stack.py
python algorithms/algorithms_queue.py
python algorithms/algorithms_deque.py
python algorithms/algorithms_linked_list.py

# Scenario analysis (requires Python 3.10+ for union type hints)
python scenario_analysis.py
```

**Python version:** 3.10 or higher required (uses `X | Y` union syntax and `match` type hints).
