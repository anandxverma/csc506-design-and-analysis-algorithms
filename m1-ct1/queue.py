# FIFO queue backed by collections.deque.
# deque gives O(1) append (enqueue) and popleft (dequeue),
# avoiding the O(n) shift cost of a plain list.
from collections import deque


class Queue:
    """First-in, first-out (FIFO) queue."""

    def __init__(self):
        self._items = deque()  # Front of queue is index 0

    def enqueue(self, item):
        """Add item to the back of the queue. O(1)."""
        self._items.append(item)

    def dequeue(self):
        """Remove and return the front item. Raises IndexError if empty. O(1)."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def peek(self):
        """Return the front item without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("peek at empty queue")
        return self._items[0]

    def is_empty(self):
        """Return True if the queue contains no items."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the queue."""
        return len(self._items)

    def __repr__(self):
        return f"Queue({list(self._items)})"


if __name__ == "__main__":
    q = Queue()

    print("Enqueue 10, 20, 30")
    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    print(q)

    print(f"Peek: {q.peek()}")
    print(f"Dequeue: {q.dequeue()}")
    print(f"After dequeue: {q}")
    print(f"Size: {q.size()}")
    print(f"Is empty: {q.is_empty()}")
