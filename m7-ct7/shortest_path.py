import heapq

from graph_adj_list import Graph as AdjListGraph
from graph_adj_matrix import Graph as AdjMatrixGraph


def _get_weighted_neighbors(graph, label):
    """Return (neighbor, weight) pairs regardless of graph representation."""
    neighbors = graph.get_neighbors(label)
    if not neighbors:
        return []
    # AdjListGraph.get_neighbors returns [(neighbor, weight), ...]
    if isinstance(neighbors[0], tuple):
        return neighbors
    # AdjMatrixGraph.get_neighbors returns [neighbor_label, ...]
    src_idx = graph.label_to_index[label]
    return [(nb, graph.matrix[src_idx][graph.label_to_index[nb]]) for nb in neighbors]


def _all_vertices(graph):
    """Return all vertex labels for either graph type."""
    if hasattr(graph, '_adj'):
        return list(graph._adj.keys())
    return list(graph.vertices)


def _reconstruct_path(pred, start_label, end_label):
    """Walk predecessor map backwards to build the path list."""
    if pred[end_label] is None and end_label != start_label:
        return []
    path = []
    current = end_label
    while current is not None:
        path.append(current)
        current = pred[current]
    path.reverse()
    return path


def dijkstra(graph, start_label):
    """
    Dijkstra's shortest path from start_label to all reachable vertices.

    Uses a min-heap priority queue and prints every edge relaxation.
    Returns (distances, predecessors).
    """
    vertices = _all_vertices(graph)
    dist = {v: float('inf') for v in vertices}
    pred = {v: None for v in vertices}
    dist[start_label] = 0

    heap = [(0, start_label)]
    visited = set()

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        for v, w in _get_weighted_neighbors(graph, u):
            new_dist = d + w
            old_dist = dist[v]
            old_str = '∞' if old_dist == float('inf') else old_dist
            print(f"  Relaxing edge {u}→{v}  old_dist={old_str}  new_dist={new_dist}")
            if new_dist < old_dist:
                dist[v] = new_dist
                pred[v] = u
                heapq.heappush(heap, (new_dist, v))

    return dist, pred


def shortest_path(graph, start_label, end_label):
    """
    Find the shortest path between two vertices.

    Returns (path as ordered vertex list, total cost).
    Returns ([], float('inf')) when no route exists.
    """
    dist, pred = dijkstra(graph, start_label)

    if dist[end_label] == float('inf'):
        return [], float('inf')

    return _reconstruct_path(pred, start_label, end_label), dist[end_label]


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    SOURCE = "A"
    VERTICES = ["A", "B", "C", "D", "E", "F", "G"]
    # Weighted directed edges: (src, dst, weight)
    EDGES = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "D", 5),
        ("B", "E", 3),
        ("C", "B", 1),
        ("C", "D", 8),
        ("C", "F", 10),
        ("D", "G", 2),
        ("E", "D", 1),
        ("E", "G", 6),
        ("F", "G", 3),
    ]

    def _build_adj_list():
        g = AdjListGraph(directed=True)
        for v in VERTICES:
            g.add_vertex(v)
        for src, dst, w in EDGES:
            g.add_edge(src, dst, w)
        return g

    def _build_adj_matrix():
        g = AdjMatrixGraph(directed=True)
        for v in VERTICES:
            g.add_vertex(v)
        for src, dst, w in EDGES:
            g.add_edge(src, dst, w)
        return g

    def _print_results(dist, pred, source, vertices):
        print(f"\n{'Destination':>12}  {'Distance':>10}  Path")
        print("-" * 55)
        for v in vertices:
            if v == source:
                continue
            d = dist[v]
            d_str = '∞' if d == float('inf') else str(d)
            path = _reconstruct_path(pred, source, v)
            path_str = ' → '.join(path) if path else 'no path'
            print(f"{v:>12}  {d_str:>10}  {path_str}")

    # ---- Adjacency-list run ------------------------------------------------
    print("=" * 55)
    print("DIJKSTRA — Adjacency List representation")
    print("=" * 55)
    g_list = _build_adj_list()
    print(f"\nRelaxation trace (source = {SOURCE}):")
    dist_list, pred_list = dijkstra(g_list, SOURCE)
    print(f"\nDistance table (source = {SOURCE}):")
    _print_results(dist_list, pred_list, SOURCE, VERTICES)

    # ---- Adjacency-matrix run ----------------------------------------------
    print("\n" + "=" * 55)
    print("DIJKSTRA — Adjacency Matrix representation")
    print("=" * 55)
    g_matrix = _build_adj_matrix()
    print(f"\nRelaxation trace (source = {SOURCE}):")
    dist_matrix, pred_matrix = dijkstra(g_matrix, SOURCE)
    print(f"\nDistance table (source = {SOURCE}):")
    _print_results(dist_matrix, pred_matrix, SOURCE, VERTICES)

    # ---- Assert both representations agree ---------------------------------
    assert dist_list == dist_matrix, (
        f"Distance mismatch!\n  list  : {dist_list}\n  matrix: {dist_matrix}"
    )
    for v in VERTICES:
        path_list = _reconstruct_path(pred_list, SOURCE, v)
        path_matrix = _reconstruct_path(pred_matrix, SOURCE, v)
        assert path_list == path_matrix, (
            f"Path mismatch for {SOURCE}→{v}:\n"
            f"  list  : {path_list}\n  matrix: {path_matrix}"
        )

    print("\n" + "=" * 55)
    print("Assertion passed: both representations yield")
    print("identical distances and paths for all vertices.")
    print("=" * 55)
