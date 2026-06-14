class PriorityQueue:
    """Min-heap based priority queue. Lowest value = highest priority."""

    def __init__(self):
        """Initialize an empty min-heap backing store."""
        self._heap = []

    def push(self, item, priority):
        """Add `item` to the queue with the given numeric `priority` (lower = higher priority)."""
        self._heap.append((priority, item))
        self._sift_up(len(self._heap) - 1)

    def pop(self):
        """Remove and return the highest-priority (lowest numeric value) item."""
        if self.is_empty():
            raise IndexError("pop from empty priority queue")
        self._swap(0, len(self._heap) - 1)
        priority, item = self._heap.pop()
        if self._heap:
            self._sift_down(0)
        return item

    def peek(self):
        """Return the highest-priority item without removing it from the queue."""
        if self.is_empty():
            raise IndexError("peek at empty priority queue")
        return self._heap[0][1]

    def is_empty(self):
        """Return True if the queue contains no items."""
        return len(self._heap) == 0

    def __len__(self):
        """Return the number of items currently in the queue."""
        return len(self._heap)

    def __repr__(self):
        """Return a sorted, human-readable representation of all (priority, item) pairs."""
        sorted_items = sorted(self._heap)
        return f"PriorityQueue([{', '.join(f'({p}, {v!r})' for p, v in sorted_items)}])"

    # --- internal heap helpers ---

    def _parent(self, i):
        """Return the heap index of node i's parent."""
        return (i - 1) // 2

    def _left(self, i):
        """Return the heap index of node i's left child."""
        return 2 * i + 1

    def _right(self, i):
        """Return the heap index of node i's right child."""
        return 2 * i + 2

    def _swap(self, i, j):
        """Swap the heap elements at indices i and j."""
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, i):
        """Bubble the element at index i up until the min-heap property is restored."""
        while i > 0:
            parent = self._parent(i)
            if self._heap[i] < self._heap[parent]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i):
        """Push the element at index i down until the min-heap property is restored."""
        size = len(self._heap)
        while True:
            smallest = i
            left, right = self._left(i), self._right(i)

            if left < size and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < size and self._heap[right] < self._heap[smallest]:
                smallest = right

            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest


if __name__ == "__main__":
    pq = PriorityQueue()

    pq.push("low urgency task", priority=10)
    pq.push("critical task", priority=1)
    pq.push("medium task", priority=5)
    pq.push("another critical", priority=1)
    pq.push("high urgency task", priority=3)

    print("Queue:", pq)
    print("Size:", len(pq))
    print("Peek (next up):", pq.peek())
    print()

    print("Processing in priority order:")
    while not pq.is_empty():
        print(" -", pq.pop())
