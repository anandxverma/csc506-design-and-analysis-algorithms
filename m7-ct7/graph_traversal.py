"""
graph_traversal.py
DFS and BFS traversal functions compatible with both graph representations
(graph_adj_matrix.py and graph_adj_list.py).
"""

from collections import deque


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _all_labels(graph):
    """Return all vertex labels for either graph representation."""
    if hasattr(graph, "vertices"):          # adjacency-matrix version
        return list(graph.vertices)
    return list(graph._adj.keys())          # adjacency-list version


def _neighbor_labels(raw_neighbors):
    """
    Normalize neighbors to a plain list of labels.
    Matrix  get_neighbors -> [label, ...]
    List    get_neighbors -> [(label, weight), ...]
    """
    if raw_neighbors and isinstance(raw_neighbors[0], tuple):
        return [nb for nb, _ in raw_neighbors]
    return list(raw_neighbors)


# ---------------------------------------------------------------------------
# Public traversal functions
# ---------------------------------------------------------------------------

def dfs(graph, start_label) -> list:
    """
    Iterative depth-first traversal starting at start_label.
    Uses an explicit stack so call-stack depth is never a constraint.
    Returns the ordered list of visited vertex labels.
    """
    visited = set()
    order = []
    stack = [start_label]
    step = 1

    while stack:
        vertex = stack.pop()
        if vertex in visited:
            continue
        visited.add(vertex)
        order.append(vertex)
        print(f"  Step {step}: Visit {vertex}")
        step += 1

        # Push neighbors in reverse so the first neighbor is visited first.
        neighbors = _neighbor_labels(graph.get_neighbors(vertex))
        for nb in reversed(neighbors):
            if nb not in visited:
                stack.append(nb)

    unvisited = [v for v in _all_labels(graph) if v not in visited]
    if unvisited:
        print(f"  [Disconnected] Unvisited vertices: {', '.join(str(v) for v in unvisited)}")

    return order


def bfs(graph, start_label) -> list:
    """
    Breadth-first traversal starting at start_label.
    Returns the ordered list of visited vertex labels.
    """
    visited = {start_label}
    order = []
    queue = deque([start_label])
    step = 1

    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        print(f"  Step {step}: Visit {vertex}")
        step += 1

        for nb in _neighbor_labels(graph.get_neighbors(vertex)):
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)

    unvisited = [v for v in _all_labels(graph) if v not in visited]
    if unvisited:
        print(f"  [Disconnected] Unvisited vertices: {', '.join(str(v) for v in unvisited)}")

    return order


# ---------------------------------------------------------------------------
# ASCII tree renderer
# ---------------------------------------------------------------------------

def _render_tree(parent: dict, root: str) -> str:
    """
    Render a discovered-edge tree as an ASCII diagram.
    parent maps child -> parent; root has no parent entry.
    """
    from collections import defaultdict

    children: dict = defaultdict(list)
    for child, par in parent.items():
        children[par].append(child)

    lines = []

    def _draw(node, prefix, is_last):
        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + str(node))
        kids = children.get(node, [])
        for i, kid in enumerate(kids):
            extension = "    " if is_last else "│   "
            _draw(kid, prefix + extension, i == len(kids) - 1)

    lines.append(str(root))
    kids = children.get(root, [])
    for i, kid in enumerate(kids):
        _draw(kid, "", i == len(kids) - 1)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Visual traversal functions
# ---------------------------------------------------------------------------

def visual_bfs(graph, start_label) -> list:
    """BFS with step-by-step frontier display and final ASCII tree."""
    visited = {start_label}
    order = []
    queue = deque([start_label])
    parent: dict = {}
    step = 1

    print(f"BFS from '{start_label}'")
    print("-" * 55)

    while queue:
        frontier_str = "[" + ", ".join(str(v) for v in queue) + "]"
        vertex = queue.popleft()
        order.append(vertex)

        discovered = []
        for nb in _neighbor_labels(graph.get_neighbors(vertex)):
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
                parent[nb] = vertex
                discovered.append(nb)

        if step == 1:
            edge_info = f"Discovered: {vertex}"
        elif discovered:
            edges = ", ".join(f"{vertex}→{nb}" for nb in discovered)
            edge_info = f"Edge: {edges}"
        else:
            edge_info = f"Visit: {vertex} (no new edges)"

        print(
            f"  Step {step:<2} | Queue: {frontier_str:<18} | Visit: {vertex}  | {edge_info}"
        )
        step += 1

    unvisited = [v for v in _all_labels(graph) if v not in visited]
    if unvisited:
        print(f"  [Disconnected] Unvisited: {', '.join(str(v) for v in unvisited)}")

    print(f"\n  Traversal tree (BFS):\n")
    for line in _render_tree(parent, start_label).splitlines():
        print("    " + line)

    return order


def visual_dfs(graph, start_label) -> list:
    """Recursive DFS with depth-indented output and final ASCII tree."""
    visited: set = set()
    order: list = []
    parent: dict = {}

    print(f"DFS from '{start_label}'")
    print("-" * 45)

    def _visit(vertex, depth):
        visited.add(vertex)
        order.append(vertex)
        indent = "  " * depth
        print(f"  {indent}[depth {depth}] Visit {vertex}")

        for nb in _neighbor_labels(graph.get_neighbors(vertex)):
            if nb not in visited:
                parent[nb] = vertex
                _visit(nb, depth + 1)
                print(f"  {'  ' * depth}[depth {depth}] Backtrack to {vertex}")

    _visit(start_label, 0)

    unvisited = [v for v in _all_labels(graph) if v not in visited]
    if unvisited:
        print(f"  [Disconnected] Unvisited: {', '.join(str(v) for v in unvisited)}")

    print(f"\n  Traversal tree (DFS):\n")
    for line in _render_tree(parent, start_label).splitlines():
        print("    " + line)

    return order


# ---------------------------------------------------------------------------
# __main__
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import os

    # Make sure sibling modules are importable when run directly.
    sys.path.insert(0, os.path.dirname(__file__))

    import graph_adj_matrix as matrix_mod
    import graph_adj_list   as list_mod

    # ------------------------------------------------------------------
    # Build the same directed graph in both representations.
    # 6 vertices, 8 directed edges.
    # ------------------------------------------------------------------
    VERTICES = ["A", "B", "C", "D", "E", "F"]
    EDGES = [
        ("A", "B"),
        ("A", "C"),
        ("B", "D"),
        ("B", "E"),
        ("C", "D"),
        ("C", "F"),
        ("D", "E"),
        ("E", "F"),
    ]
    START = "A"

    gm = matrix_mod.Graph(directed=True)
    gl = list_mod.Graph(directed=True)

    for v in VERTICES:
        gm.add_vertex(v)
        gl.add_vertex(v)

    for src, dst in EDGES:
        gm.add_edge(src, dst)
        gl.add_edge(src, dst)

    print("=" * 60)
    print("Directed graph — adjacency matrix:")
    gm.display()

    print("\nDirected graph — adjacency list:")
    gl.display()

    # ------------------------------------------------------------------
    # DFS on both representations
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"DFS from '{START}' — adjacency MATRIX:")
    dfs_matrix = dfs(gm, START)

    print(f"\nDFS from '{START}' — adjacency LIST:")
    dfs_list = dfs(gl, START)

    # ------------------------------------------------------------------
    # BFS on both representations
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"BFS from '{START}' — adjacency MATRIX:")
    bfs_matrix = bfs(gm, START)

    print(f"\nBFS from '{START}' — adjacency LIST:")
    bfs_list = bfs(gl, START)

    # ------------------------------------------------------------------
    # Assertions
    # ------------------------------------------------------------------
    assert dfs_matrix == dfs_list, (
        f"DFS mismatch!\n  matrix: {dfs_matrix}\n  list:   {dfs_list}"
    )
    assert bfs_matrix == bfs_list, (
        f"BFS mismatch!\n  matrix: {bfs_matrix}\n  list:   {bfs_list}"
    )
    print("\n[OK] Both representations produce identical traversal orders.")

    # ------------------------------------------------------------------
    # Visual traversals on the adjacency-list graph
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("VISUAL BFS")
    print("=" * 60)
    visual_bfs(gl, START)

    print("\n" + "=" * 60)
    print("VISUAL DFS")
    print("=" * 60)
    visual_dfs(gl, START)

    # ------------------------------------------------------------------
    # Side-by-side comparison table
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Side-by-side traversal comparison")
    print("=" * 60)

    col = 12
    header = (
        f"{'Step':<6}"
        f"{'DFS (matrix)':<{col}}"
        f"{'DFS (list)':<{col}}"
        f"{'BFS (matrix)':<{col}}"
        f"{'BFS (list)':<{col}}"
    )
    print(header)
    print("-" * len(header))

    n = max(len(dfs_matrix), len(bfs_matrix))
    for i in range(n):
        dm = dfs_matrix[i] if i < len(dfs_matrix) else "-"
        dl = dfs_list[i]   if i < len(dfs_list)   else "-"
        bm = bfs_matrix[i] if i < len(bfs_matrix) else "-"
        bl = bfs_list[i]   if i < len(bfs_list)   else "-"
        print(
            f"{i + 1:<6}"
            f"{dm:<{col}}"
            f"{dl:<{col}}"
            f"{bm:<{col}}"
            f"{bl:<{col}}"
        )

    print("=" * 60)
