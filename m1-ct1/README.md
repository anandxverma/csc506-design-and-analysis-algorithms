# CSC 506 — Design and Analysis of Algorithms
# Critical Thinking Assignment 1

Interactive tool for Data Structure visualization and Performance Benchmarking.
---

## Project Structure

```
csc506-design-and-analysis-algorithms/
└── ct1/
    ├── linked_list.py   # Singly linked list implementation
    ├── stack.py         # LIFO stack implementation
    ├── queue.py         # FIFO queue implementation
    ├── benchmark.py     # Performance benchmarking framework
    ├── gui.py           # Interactive Tkinter GUI
    ├── ui.py            # Terminal (TUI) interface
    └── demo.py          # Automated GUI demo for screen recording
```

---

## Requirements

**Python 3.8 or Above+**

Most files use only the Python standard library. The GUI and demo require `matplotlib`:

```bash
pip install matplotlib
```

---

## Running the GUI

```bash
cd ct1
python3 gui.py
```

Launches an interactive 5-tab window (880×680):

| Tab | Description |
|-----|-------------|
| Stack | Visual stack — Push, Pop, Peek, Clear |
| Queue | Visual queue — Enqueue, Dequeue, Peek, Clear |
| Linked List | Visual linked list — Append, Prepend, Delete, Search, Clear |
| Complexity | Big-O reference table with click-to-explain rows |
| Performance | Live benchmark runner with measured vs. predicted O(1)/O(n) charts |

---

## Running the Automated Demo

```bash
cd ct1
python3 demo.py          # Full demo (~4 min 45 sec), suitable for screen recording
python3 demo.py --fast   # Accelerated playback for testing
```

Drives the GUI automatically through all 5 tabs — stack pushes, queue operations, linked list mutations, complexity highlights, and a live benchmark run. Close the window to stop at any time.

---

## Running the Terminal UI

```bash
cd ct1
python3 ui.py
```

Menu-driven terminal interface with colored ANSI output and ASCII art visualizations for all three data structures. No external dependencies required.

---

## Running the Data Structure Modules Directly

Each module has a self-test that runs when executed directly:

```bash
cd ct1
python3 stack.py        # Push / pop / peek self-test
python3 queue.py        # Enqueue / dequeue / peek self-test
python3 linked_list.py  # Append / prepend / delete / search self-test
```

---

## Running the Benchmark

```bash
cd ct1
python3 benchmark.py
```

Benchmarks all three data structures across input sizes from 100 to 50,000 elements (7 repetitions each). Prints progress to the console and reports measured times alongside fitted O(1) and O(n) predictions. Takes a few minutes to complete.

---

## Data Structures Covered

| Structure | Operations | Complexity |
|-----------|-----------|------------|
| Stack | Push, Pop, Peek | O(1) all |
| Queue | Enqueue, Dequeue, Peek | O(1) all |
| Linked List | Prepend | O(1) |
| | Append, Search, Delete | O(n) |
