class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self._adj = {}  # label -> [(neighbor_label, weight), ...]

    # -- internal helper ---------------------------------------------------

    def _check(self, label):
        if label not in self._adj:
            raise ValueError(f"Unknown vertex: {label!r}")

    # -- vertex operations -------------------------------------------------

    def add_vertex(self, label):
        if label in self._adj:
            raise ValueError(f"Vertex already exists: {label!r}")
        self._adj[label] = []

    def remove_vertex(self, label):
        self._check(label)
        del self._adj[label]
        for neighbors in self._adj.values():
            neighbors[:] = [(nb, w) for nb, w in neighbors if nb != label]

    # -- edge operations ---------------------------------------------------

    def add_edge(self, src, dst, weight=1):
        self._check(src)
        self._check(dst)
        self._adj[src].append((dst, weight))
        if not self.directed:
            self._adj[dst].append((src, weight))

    def remove_edge(self, src, dst):
        self._check(src)
        self._check(dst)
        self._adj[src] = [(nb, w) for nb, w in self._adj[src] if nb != dst]
        if not self.directed:
            self._adj[dst] = [(nb, w) for nb, w in self._adj[dst] if nb != src]

    def has_edge(self, src, dst):
        self._check(src)
        self._check(dst)
        return any(nb == dst for nb, _ in self._adj[src])

    # -- query -------------------------------------------------------------

    def get_neighbors(self, label):
        self._check(label)
        return list(self._adj[label])

    # -- display -----------------------------------------------------------

    def display(self):
        for label, neighbors in self._adj.items():
            nb_str = " -> ".join(f"{nb}({w})" for nb, w in neighbors) or "None"
            print(f"  {label}: {nb_str}")


if __name__ == "__main__":
    g = Graph(directed=False)

    for v in ("A", "B", "C", "D", "E"):
        g.add_vertex(v)

    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "E")]
    for src, dst in edges:
        g.add_edge(src, dst)

    print("Graph after adding 5 vertices and 6 edges:")
    g.display()

    print(f"\nNeighbors of C: {g.get_neighbors('C')}")
    print(f"has_edge(A, B): {g.has_edge('A', 'B')}")
    print(f"has_edge(A, E): {g.has_edge('A', 'E')}")

    print("\nRemoving vertex B...")
    g.remove_vertex("B")

    print("\nGraph after removing B:")
    g.display()

    print("\n--- Directed graph demo ---")
    dg = Graph(directed=True)
    for v in ("A", "B", "C", "D", "E"):
        dg.add_vertex(v)
    for src, dst in edges:
        dg.add_edge(src, dst)

    print("Directed graph:")
    dg.display()
    print(f"\nhas_edge(A, B): {dg.has_edge('A', 'B')}")
    print(f"has_edge(B, A): {dg.has_edge('B', 'A')}  (directed — no back-edge)")
