# Singly linked list implementation.
# Each node holds data and a pointer to the next node.
# Operations: append, prepend, delete, search — all O(n) except prepend O(1).


class Node:
    # A single element in the linked list.
    def __init__(self, data):
        self.data = data
        self.next = None  # Points to the next node; None marks the tail


class LinkedList:
    """Singly linked list with head pointer and size tracking."""

    def __init__(self):
        self._head = None  # First node in the list
        self._size = 0

    def append(self, data):
        """Add node to the end. O(n) — traverses to the tail."""
        new_node = Node(data)
        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def prepend(self, data):
        """Add node to the front. O(1)."""
        new_node = Node(data)
        new_node.next = self._head
        self._head = new_node
        self._size += 1

    def delete(self, data):
        """Remove first node with matching data. Raises ValueError if not found."""
        if self._head is None:
            raise ValueError(f"{data} not found in list")

        # Special case: target is the head node
        if self._head.data == data:
            self._head = self._head.next
            self._size -= 1
            return

        # Walk list keeping a reference to the predecessor so we can re-link
        current = self._head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return
            current = current.next

        raise ValueError(f"{data} not found in list")

    def search(self, data):
        """Return True if data exists in the list, False otherwise. O(n)."""
        current = self._head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def to_list(self):
        """Return all node values as a Python list, preserving order."""
        result = []
        current = self._head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def is_empty(self):
        """Return True if the list contains no nodes."""
        return self._size == 0

    def size(self):
        """Return the number of nodes in the list."""
        return self._size

    def __repr__(self):
        nodes = " -> ".join(str(item) for item in self.to_list())
        return f"LinkedList([{nodes}])"


if __name__ == "__main__":
    ll = LinkedList()

    print("Append 10, 20, 30")
    ll.append(10)
    ll.append(20)
    ll.append(30)
    print(ll)

    print("Prepend 5")
    ll.prepend(5)
    print(ll)

    print(f"Search 20: {ll.search(20)}")
    print(f"Search 99: {ll.search(99)}")

    print("Delete 20")
    ll.delete(20)
    print(ll)

    print(f"Size: {ll.size()}")
    print(f"Is empty: {ll.is_empty()}")
