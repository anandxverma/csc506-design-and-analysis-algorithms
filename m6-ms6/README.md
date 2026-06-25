# Module 6 — Binary Search Tree & Performance Analysis

**Course:** CSC 506 · Design and Analysis of Algorithms

---

## Setup

Python 3.8+ is required. Most files use only the standard library. The PDF report generator has two extra dependencies:

```bash
pip install matplotlib reportlab
```

To install into a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install matplotlib reportlab
```

---

## Files

### [bst.py](bst.py)
Core data structure module containing two classes:

**`binary_tree_search`** — A full-featured Binary Search Tree (BST).

| Method | Description | Time |
|---|---|---|
| `insert(key)` | Insert a key; duplicates are ignored | O(h) |
| `search(key)` | Return `True`/`False` | O(h) |
| `delete(key)` | Remove a key (handles all 3 cases) | O(h) |
| `find_min()` / `find_max()` | Leftmost / rightmost key | O(h) |
| `height()` | Longest root-to-leaf edge count | O(n) |
| `is_valid_bst()` | Verify BST property on every node | O(n) |
| `find_kth_smallest(k)` | 1-indexed k-th smallest key | O(h + k) |
| `is_balanced()` | AVL balance check (|bf| ≤ 1 everywhere) | O(n) |
| `node_balance_factor(key)` | Balance factor for one node | O(h) |
| `balance_report()` | Full balance summary dict | O(n²) |
| `inorder()` | Keys ascending (left → node → right) | O(n) |
| `preorder()` | Keys root-first (node → left → right) | O(n) |
| `postorder()` | Keys leaves-first (left → right → node) | O(n) |
| `level_order()` | Breadth-first level by level | O(n) |
| `print_tree(label)` | ASCII diagram to stdout | O(n) |

*h = tree height: O(log n) for balanced trees, O(n) worst-case (sorted insertion).*

**`Map`** — An ordered key-value store backed by the BST above.  
Supports `put`, `get`, `get_or_default`, `delete`, `contains_key`, `keys()`, `values()`, `items()`, `size()`, and the standard Python protocols (`[]`, `in`, `del`, `len`, `iter`).

```bash
python bst.py
```
Runs a built-in demo: step-by-step insertions/deletions with ASCII tree diagrams, traversal output, balance detection, and the `Map` key-value store.

---

### [performance_analysis.py](performance_analysis.py)
Benchmarks BST-backed `Map` vs. a naïve `ListMap` (linear-scan list of pairs).

**What it measures:**

| Scenario | Insertion order | Search type |
|---|---|---|
| Average case | Random-shuffled | Hit (key present) |
| Average case | Random-shuffled | Miss (key absent) |
| Worst case | Sorted ascending | Hit |
| Worst case | Sorted ascending | Miss |

Dataset sizes: **100, 500, 1,000, 5,000, 10,000**  
Each cell: average of 500 × 50 = 25,000 `contains_key()` calls, reported in **µs**.

```bash
python performance_analysis.py
```
Prints a formatted table with BST vs. List timings and a complexity-growth analysis showing O(log n) vs. O(n) behaviour.

---

### [generate_report.py](generate_report.py)
Runs the benchmarks from `performance_analysis.py` and writes a multi-page **PDF report**.

The PDF includes:
- Cover / executive summary
- Raw timing table (all 10 scenarios)
- Five charts (hit latency, miss latency, sorted worst-case, speed ratios, log-scale comparison)
- Complexity growth analysis tables
- Theoretical complexity summary and conclusions

**Dependencies:** `matplotlib`, `reportlab`

```bash
pip install matplotlib reportlab
python generate_report.py
# → prompts for output path, defaults to ./report.pdf
```

> **Note:** `bst.py`, `performance_analysis.py`, and `test_bst.py` use only the Python standard library and require no additional packages.

---

### [test_bst.py](test_bst.py)
`unittest` test suite for `binary_tree_search`.

| Test class | Data set | Coverage |
|---|---|---|
| `TestIntegerBST` | 25 integers (negative, zero, large) | insert, search, delete, all traversals, min/max, height, kth-smallest, balance |
| `TestFloatBST` | 15 floats | all operations on float keys |
| `TestStringBST` | 15 strings | lexicographic ordering, case-sensitivity |
| `TestEdgeCases` | various | empty tree, single node, right-skewed, left-skewed, perfectly balanced |
| `TestTraversalRelationships` | complete BST [50,30,70,20,40,60,80] | structural invariants between traversal orders |

```bash
python -m unittest test_bst.py -v
```

---

## Complexity Reference

| Structure | Insert | Search — avg | Search — worst |
|---|---|---|---|
| BST `Map` (random insertion) | O(log n) | O(log n) | O(n) |
| BST `Map` (sorted insertion) | O(n) | O(n) | O(n) |
| `ListMap` | O(n) | O(n) | O(n) |

**Key takeaway:** A randomly-built BST dominates the list for search at every dataset size. Sorted insertion degenerates the BST into a right-skewed chain of height n − 1, collapsing performance to O(n). Use a self-balancing tree (AVL, Red-Black) when insertion order is not controlled.
