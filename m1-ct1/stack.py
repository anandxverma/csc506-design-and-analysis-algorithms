# LIFO stack backed by a Python list.
# list.append and list.pop operate on the tail, both O(1),
# making it a natural fit for a stack without extra overhead.


class Stack:
    """Last-in, first-out (LIFO) stack."""

    def __init__(self):
        self._items = []  # Top of stack is the last element

    def push(self, item):
        """Push item onto the top of the stack. O(1) amortized."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item. Raises IndexError if empty. O(1)."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self):
        """Return True if the stack contains no items."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"


if __name__ == "__main__":
    s = Stack()

    print("Push 10, 20, 30")
    s.push(10)
    s.push(20)
    s.push(30)
    print(s)

    print(f"Peek: {s.peek()}")
    print(f"Pop: {s.pop()}")
    print(f"After pop: {s}")
    print(f"Size: {s.size()}")
    print(f"Is empty: {s.is_empty()}")
