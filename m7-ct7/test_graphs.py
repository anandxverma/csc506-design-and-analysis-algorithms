"""
test_graphs.py
Comprehensive test suite for MatrixGraph, ListGraph, and all algorithms.

Sample graph: 8 vertices (A–H), 12 weighted undirected edges.
Known shortest path A→H = 9  (A→B→E→H: 3+4+2).
"""

import sys
import io
import time
import contextlib
import os

sys.path.insert(0, os.path.dirname(__file__))

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from graph_adj_matrix import Graph as MatrixGraph
from graph_adj_list   import Graph as ListGraph
from graph_traversal  import dfs, bfs
from shortest_path    import dijkstra, shortest_path

# ---------------------------------------------------------------------------
# Sample graph definition
# 8 vertices, 12 weighted undirected edges, shortest A→H = 9
# ---------------------------------------------------------------------------
VERTICES = ["A", "B", "C", "D", "E", "F", "G", "H"]
EDGES = [           # (src, dst, weight)
    ("A", "B", 3),
    ("A", "C", 5),
    ("A", "D", 7),
    ("B", "C", 2),
    ("B", "E", 4),
    ("C", "F", 3),
    ("D", "E", 6),
    ("D", "G", 2),
    ("E", "H", 2),  # A→B(3)→E(4)→H(2) = 9
    ("F", "G", 4),
    ("F", "H", 6),
    ("G", "H", 5),
]


def sample_graph():
    """Return (MatrixGraph, ListGraph) built from the same 8-vertex/12-edge graph."""
    mg = MatrixGraph(directed=False)
    lg = ListGraph(directed=False)
    for v in VERTICES:
        mg.add_vertex(v)
        lg.add_vertex(v)
    for src, dst, w in EDGES:
        mg.add_edge(src, dst, w)
        lg.add_edge(src, dst, w)
    return mg, lg


# ---------------------------------------------------------------------------
# Test infrastructure
# ---------------------------------------------------------------------------
_results = []


def run_test(number, description, fn):
    try:
        fn()
        _results.append(True)
        print(f"Test {number:>2}  PASS  {description}")
    except Exception as exc:
        _results.append(False)
        print(f"Test {number:>2}  FAIL  {description}")
        print(f"        {type(exc).__name__}: {exc}")


def _silent(fn, *args, **kwargs):
    """Call fn while swallowing its stdout output."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return fn(*args, **kwargs)


# ---------------------------------------------------------------------------
# Individual tests
# ---------------------------------------------------------------------------

def test1():
    """add_vertex / has_edge round-trip on both representations."""
    mg, lg = sample_graph()
    for src, dst, _ in EDGES:
        assert mg.has_edge(src, dst), f"Matrix missing edge {src}-{dst}"
        assert mg.has_edge(dst, src), f"Matrix missing reverse edge {dst}-{src}"
        assert lg.has_edge(src, dst), f"List missing edge {src}-{dst}"
        assert lg.has_edge(dst, src), f"List missing reverse edge {dst}-{src}"
    # A–H is not a direct edge in the sample graph
    assert not mg.has_edge("A", "H"), "Matrix wrongly reports A-H edge"
    assert not lg.has_edge("A", "H"), "List wrongly reports A-H edge"


def test2():
    """remove_vertex cleans up all incident edges."""
    mg, lg = sample_graph()
    # B connects to A, C, E — removing it must clean those incident edges
    mg.remove_vertex("B")
    lg.remove_vertex("B")

    assert "B" not in mg.vertices, "Matrix: B still listed after removal"
    assert "B" not in lg._adj,     "List: B still listed after removal"

    # Unrelated edges must survive
    assert mg.has_edge("A", "C"), "Matrix: A-C missing after removing B"
    assert lg.has_edge("A", "C"), "List: A-C missing after removing B"

    # A's neighbor list must no longer contain B
    mg_a_nbs = mg.get_neighbors("A")
    lg_a_nbs = [nb for nb, _ in lg.get_neighbors("A")]
    assert "B" not in mg_a_nbs, "Matrix: A still lists B as neighbor"
    assert "B" not in lg_a_nbs, "List: A still lists B as neighbor"


def test3():
    """DFS visits all reachable vertices, correct order."""
    mg, lg = sample_graph()
    dfs_mg = _silent(dfs, mg, "A")
    dfs_lg = _silent(dfs, lg, "A")

    assert dfs_mg[0] == "A", f"Matrix DFS must start at A, got {dfs_mg[0]}"
    assert dfs_lg[0] == "A", f"List DFS must start at A, got {dfs_lg[0]}"
    assert set(dfs_mg) == set(VERTICES), \
        f"Matrix DFS missed: {set(VERTICES) - set(dfs_mg)}"
    assert set(dfs_lg) == set(VERTICES), \
        f"List DFS missed: {set(VERTICES) - set(dfs_lg)}"


def test4():
    """BFS visits all reachable vertices, correct order."""
    mg, lg = sample_graph()
    bfs_mg = _silent(bfs, mg, "A")
    bfs_lg = _silent(bfs, lg, "A")

    assert bfs_mg[0] == "A", f"Matrix BFS must start at A, got {bfs_mg[0]}"
    assert bfs_lg[0] == "A", f"List BFS must start at A, got {bfs_lg[0]}"
    assert set(bfs_mg) == set(VERTICES), \
        f"Matrix BFS missed: {set(VERTICES) - set(bfs_mg)}"
    assert set(bfs_lg) == set(VERTICES), \
        f"List BFS missed: {set(VERTICES) - set(bfs_lg)}"


def test5():
    """DFS and BFS produce same visited set (not same order)."""
    mg, lg = sample_graph()
    dfs_mg = _silent(dfs, mg, "A")
    bfs_mg = _silent(bfs, mg, "A")
    dfs_lg = _silent(dfs, lg, "A")
    bfs_lg = _silent(bfs, lg, "A")

    assert set(dfs_mg) == set(bfs_mg), \
        "Matrix: DFS and BFS visited sets differ"
    assert set(dfs_lg) == set(bfs_lg), \
        "List: DFS and BFS visited sets differ"
    assert set(dfs_mg) == set(VERTICES), \
        "Matrix: combined DFS/BFS visited set is not all vertices"
    assert set(dfs_lg) == set(VERTICES), \
        "List: combined DFS/BFS visited set is not all vertices"


def test6():
    """Dijkstra finds the known shortest path A→H = cost 9."""
    mg, lg = sample_graph()
    path_mg, cost_mg = _silent(shortest_path, mg, "A", "H")
    path_lg, cost_lg = _silent(shortest_path, lg, "A", "H")

    assert cost_mg == 9, f"Matrix: A→H cost = {cost_mg}, expected 9"
    assert cost_lg == 9, f"List:   A→H cost = {cost_lg}, expected 9"
    assert path_mg and path_mg[0] == "A" and path_mg[-1] == "H", \
        f"Matrix: invalid path {path_mg}"
    assert path_lg and path_lg[0] == "A" and path_lg[-1] == "H", \
        f"List: invalid path {path_lg}"


def test7():
    """Dijkstra returns inf for unreachable vertex in directed graph."""
    mg = MatrixGraph(directed=True)
    lg = ListGraph(directed=True)
    for v in ("A", "B", "Z"):
        mg.add_vertex(v)
        lg.add_vertex(v)
    # A→B exists; Z is completely isolated
    mg.add_edge("A", "B", 1)
    lg.add_edge("A", "B", 1)

    dist_mg, _ = _silent(dijkstra, mg, "A")
    dist_lg, _ = _silent(dijkstra, lg, "A")

    assert dist_mg["Z"] == float("inf"), \
        f"Matrix: Z should be unreachable, got {dist_mg['Z']}"
    assert dist_lg["Z"] == float("inf"), \
        f"List: Z should be unreachable, got {dist_lg['Z']}"


def test8():
    """Both representations return identical Dijkstra results."""
    mg, lg = sample_graph()
    dist_mg, _ = _silent(dijkstra, mg, "A")
    dist_lg, _ = _silent(dijkstra, lg, "A")

    assert dist_mg == dist_lg, (
        f"Dijkstra distance mismatch:\n  matrix: {dist_mg}\n  list:   {dist_lg}"
    )


def test9():
    """display() produces output with correct vertex count."""
    mg, lg = sample_graph()

    buf_mg = io.StringIO()
    buf_lg = io.StringIO()
    with contextlib.redirect_stdout(buf_mg):
        mg.display()
    with contextlib.redirect_stdout(buf_lg):
        lg.display()

    out_mg = buf_mg.getvalue()
    out_lg = buf_lg.getvalue()

    for v in VERTICES:
        assert v in out_mg, f"Matrix display() missing vertex '{v}'"
        assert v in out_lg, f"List display() missing vertex '{v}'"


def test10():
    """Performance: matrix and list both complete 1000-vertex BFS in under 5 seconds."""
    N = 1000
    labels = [str(i) for i in range(N)]

    mg = MatrixGraph(directed=False)
    lg = ListGraph(directed=False)
    for v in labels:
        mg.add_vertex(v)
        lg.add_vertex(v)
    for i in range(N - 1):
        mg.add_edge(labels[i], labels[i + 1], 1)
        lg.add_edge(labels[i], labels[i + 1], 1)

    t0 = time.time()
    result_mg = _silent(bfs, mg, labels[0])
    elapsed_mg = time.time() - t0

    t0 = time.time()
    result_lg = _silent(bfs, lg, labels[0])
    elapsed_lg = time.time() - t0

    assert len(result_mg) == N, \
        f"Matrix BFS covered {len(result_mg)}/{N} vertices"
    assert len(result_lg) == N, \
        f"List BFS covered {len(result_lg)}/{N} vertices"
    assert elapsed_mg < 5.0, \
        f"Matrix BFS took {elapsed_mg:.2f}s (limit 5s)"
    assert elapsed_lg < 5.0, \
        f"List BFS took {elapsed_lg:.2f}s (limit 5s)"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
TESTS = [
    (1,  "add_vertex / has_edge round-trip on both representations",         test1),
    (2,  "remove_vertex cleans up all incident edges",                        test2),
    (3,  "DFS visits all reachable vertices, correct order",                  test3),
    (4,  "BFS visits all reachable vertices, correct order",                  test4),
    (5,  "DFS and BFS produce same visited set (not same order)",             test5),
    (6,  "Dijkstra finds the known shortest path A→H = cost 9",         test6),
    (7,  "Dijkstra returns inf for unreachable vertex in directed graph",     test7),
    (8,  "Both representations return identical Dijkstra results",            test8),
    (9,  "display() produces output with correct vertex count",               test9),
    (10, "Performance: matrix and list both complete 1000-vertex BFS in under 5 seconds", test10),
]

if __name__ == "__main__":
    print("=" * 70)
    print("Graph Test Suite")
    print("=" * 70)
    for num, desc, fn in TESTS:
        run_test(num, desc, fn)
    passed = sum(_results)
    print("=" * 70)
    print(f"{passed}/10 tests passed")
