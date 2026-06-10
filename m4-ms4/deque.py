# Double-ended queue (Deque) backed by a Python list.
# The rear is the tail (index -1) and the front is the head (index 0).
# addRear / removeRear are O(1) amortized; addFront / removeFront are O(n)
# because inserting or removing at index 0 shifts all existing elements.


class Deque:
    """Double-ended queue supporting insertion and removal at both ends."""

    def __init__(self):
        self._items = []  # front = index 0, rear = index -1

    def addFront(self, item):
        """Insert item at the front. O(n) due to list shift."""
        self._items.insert(0, item)

    def addRear(self, item):
        """Insert item at the rear. O(1) amortized."""
        self._items.append(item)

    def removeFront(self):
        """Remove and return the front item. Raises IndexError if empty. O(n)."""
        if self.isEmpty():
            raise IndexError("removeFront from empty deque")
        return self._items.pop(0)

    def removeRear(self):
        """Remove and return the rear item. Raises IndexError if empty. O(1)."""
        if self.isEmpty():
            raise IndexError("removeRear from empty deque")
        return self._items.pop()

    def isEmpty(self):
        """Return True if the deque contains no items."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the deque."""
        return len(self._items)

    def __repr__(self):
        return f"Deque(front={self._items}=rear)"


if __name__ == "__main__":
    d = Deque()

    print("addRear 10, 20, 30")
    d.addRear(10)
    d.addRear(20)
    d.addRear(30)
    print(d)  # front=[10, 20, 30]=rear

    print("addFront 5")
    d.addFront(5)
    print(d)  # front=[5, 10, 20, 30]=rear

    print(f"removeFront: {d.removeFront()}")   # 5
    print(f"removeRear:  {d.removeRear()}")    # 30
    print(f"After removals: {d}")
    print(f"Size: {d.size()}")
    print(f"isEmpty: {d.isEmpty()}")
