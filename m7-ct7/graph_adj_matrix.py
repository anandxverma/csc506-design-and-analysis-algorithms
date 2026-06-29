class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.vertices = []          # ordered list of labels
        self.label_to_index = {}    # O(1) label -> index lookup
        self.matrix = []            # 2D list of weights (0 = no edge)

    # -- internal helpers --------------------------------------------------

    def _index(self, label):
        if label not in self.label_to_index:
            raise ValueError(f"Unknown vertex: {label!r}")
        return self.label_to_index[label]

    def _rebuild_index(self):
        self.label_to_index = {label: i for i, label in enumerate(self.vertices)}

    # -- vertex operations -------------------------------------------------

    def add_vertex(self, label):
        if label in self.label_to_index:
            raise ValueError(f"Vertex already exists: {label!r}")
        n = len(self.vertices)
        self.label_to_index[label] = n
        self.vertices.append(label)
        # extend each existing row
        for row in self.matrix:
            row.append(0)
        # add a new all-zero row
        self.matrix.append([0] * (n + 1))

    def remove_vertex(self, label):
        idx = self._index(label)
        # remove the row
        self.matrix.pop(idx)
        # remove the column from every remaining row
        for row in self.matrix:
            row.pop(idx)
        self.vertices.pop(idx)
        self._rebuild_index()

    # -- edge operations ---------------------------------------------------

    def add_edge(self, src, dst, weight=1):
        i, j = self._index(src), self._index(dst)
        self.matrix[i][j] = weight
        if not self.directed:
            self.matrix[j][i] = weight

    def remove_edge(self, src, dst):
        i, j = self._index(src), self._index(dst)
        self.matrix[i][j] = 0
        if not self.directed:
            self.matrix[j][i] = 0

    def has_edge(self, src, dst):
        i, j = self._index(src), self._index(dst)
        return self.matrix[i][j] != 0

    # -- query -------------------------------------------------------------

    def get_neighbors(self, label):
        idx = self._index(label)
        return [
            self.vertices[j]
            for j, weight in enumerate(self.matrix[idx])
            if weight != 0
        ]

    # -- display -----------------------------------------------------------

    def display(self):
        col_w = max((len(str(v)) for v in self.vertices), default=1) + 1
        header = " " * (col_w + 1) + "  ".join(str(v).rjust(col_w) for v in self.vertices)
        print(header)
        separator = " " * (col_w + 1) + "--".join("-" * col_w for _ in self.vertices)
        print(separator)
        for label, row in zip(self.vertices, self.matrix):
            cells = "  ".join(str(w).rjust(col_w) for w in row)
            print(f"{str(label).rjust(col_w)} | {cells}")


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
