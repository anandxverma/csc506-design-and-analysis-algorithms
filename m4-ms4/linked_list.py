class Node:
    """A single node in a singly linked list."""

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Singly linked list with insert, delete, search, and display operations."""

    def __init__(self):
        self._head = None
        self._size = 0

    def insert(self, data, index=None):
        """Insert data at the given index (default: end). O(n)."""
        new_node = Node(data)

        if index is None:
            index = self._size

        if index < 0 or index > self._size:
            raise IndexError(f"index {index} out of range for list of size {self._size}")

        if index == 0:
            new_node.next = self._head
            self._head = new_node
        else:
            current = self._head
            for _ in range(index - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node

        self._size += 1

    def delete(self, data):
        """Remove the first node whose data equals `data`. Raises ValueError if not found. O(n)."""
        current = self._head
        prev = None

        while current is not None:
            if current.data == data:
                if prev is None:
                    self._head = current.next
                else:
                    prev.next = current.next
                self._size -= 1
                return
            prev = current
            current = current.next

        raise ValueError(f"{data!r} not found in list")

    def search(self, data):
        """Return the 0-based index of the first node with matching data, or -1 if absent. O(n)."""
        current = self._head
        index = 0
        while current is not None:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def display(self):
        """Print all elements from head to tail."""
        elements = []
        current = self._head
        while current is not None:
            elements.append(repr(current.data))
            current = current.next
        print("HEAD -> " + " -> ".join(elements) + " -> None")

    def is_empty(self):
        """Return True if the list contains no nodes."""
        return self._size == 0

    def size(self):
        """Return the number of nodes in the list."""
        return self._size

    def __repr__(self):
        elements = []
        current = self._head
        while current is not None:
            elements.append(repr(current.data))
            current = current.next
        return "LinkedList([" + ", ".join(elements) + "])"


if __name__ == "__main__":
    ll = LinkedList()

    print("Insert 10, 20, 30 at end")
    ll.insert(10)
    ll.insert(20)
    ll.insert(30)
    ll.display()

    print("Insert 5 at index 0 (new head)")
    ll.insert(5, 0)
    ll.display()

    print("Insert 15 at index 2")
    ll.insert(15, 2)
    ll.display()

    print(f"Search 15: index {ll.search(15)}")
    print(f"Search 99: index {ll.search(99)}")

    print("Delete 15")
    ll.delete(15)
    ll.display()

    print("Delete head (5)")
    ll.delete(5)
    ll.display()

    print(f"Size: {ll.size()}")
    print(f"Is empty: {ll.is_empty()}")

    print("Delete remaining nodes")
    ll.delete(10)
    ll.delete(20)
    ll.delete(30)
    print(f"Is empty after clearing: {ll.is_empty()}")
