# FIFO queue backed by a Python list.
# enqueue uses list.append (tail, O(1) amortized).
# dequeue uses list.pop(0) (head, O(n)) — acceptable for coursework;
# use collections.deque for O(1) dequeue in production.


class Queue:
    """First-in, first-out (FIFO) queue."""

    def __init__(self):
        self._items = []  # Front of queue is index 0

    def enqueue(self, item):
        """Add item to the rear of the queue. O(1) amortized."""
        self._items.append(item)

    def dequeue(self):
        """Remove and return the front item. Raises IndexError if empty. O(n)."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def front(self):
        """Return the front item without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("front of empty queue")
        return self._items[0]

    def is_empty(self):
        """Return True if the queue contains no items."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the queue."""
        return len(self._items)

    def __repr__(self):
        return f"Queue({self._items})"


if __name__ == "__main__":
    q = Queue()

    print("Enqueue 10, 20, 30")
    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    print(q)

    print(f"Front: {q.front()}")
    print(f"Dequeue: {q.dequeue()}")
    print(f"After dequeue: {q}")
    print(f"Size: {q.size()}")
    print(f"Is empty: {q.is_empty()}")
