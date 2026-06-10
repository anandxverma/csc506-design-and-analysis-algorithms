"""
Linked-list algorithms — three problems where pointer manipulation and
sequential node access make the linked list the natural structure.

Imports Node and LinkedList from linked_list.py in the same package.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from linked_list import Node, LinkedList


# ---------------------------------------------------------------------------
# Algorithm 1: Floyd's Cycle Detection (Tortoise and Hare)
# ---------------------------------------------------------------------------

def has_cycle(ll: LinkedList) -> bool:
    """
    Detect a cycle using Floyd's two-pointer algorithm.

    A slow pointer advances one node per step; a fast pointer advances two.
    If no cycle exists, the fast pointer reaches None and the function returns
    False.  If a cycle exists, the fast pointer laps the slow one and they
    meet inside the loop — returning True.
    Time: O(N)  Space: O(1)
    """
    slow = ll._head
    fast = ll._head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def cycle_entry(ll: LinkedList):
    """
    Return the data stored at the node where the cycle begins, or None.

    After Floyd's meeting point is found, resetting the slow pointer to the
    head and advancing both pointers one step at a time guarantees they
    converge exactly at the cycle's entry node.
    Time: O(N)  Space: O(1)
    """
    slow = ll._head
    fast = ll._head
    met = False
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            met = True
            break
    if not met:
        return None
    slow = ll._head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow.data


def _inject_cycle(ll: LinkedList, target_index: int) -> None:
    """Wire the tail's next pointer to the node at target_index to create a cycle."""
    if ll._head is None:
        return
    target = ll._head
    for _ in range(target_index):
        if target.next is None:
            raise IndexError("target_index out of range")
        target = target.next
    tail = ll._head
    while tail.next is not None:
        tail = tail.next
    tail.next = target


def _display_no_cycle(ll: LinkedList, limit: int = 20) -> str:
    """Return a bounded string representation safe to call on a cyclic list."""
    elements = []
    current = ll._head
    seen = set()
    count = 0
    while current is not None and count < limit:
        node_id = id(current)
        if node_id in seen:
            elements.append(f"-> [{current.data}] (cycle back)")
            break
        seen.add(node_id)
        elements.append(repr(current.data))
        current = current.next
        count += 1
    return "HEAD -> " + " -> ".join(elements)


# ---------------------------------------------------------------------------
# Algorithm 2: In-Place Linked List Reversal
# ---------------------------------------------------------------------------

def reverse(ll: LinkedList) -> None:
    """
    Reverse the linked list in-place in O(N) time and O(1) auxiliary space.

    Three local pointer variables (prev, current, nxt) are used to re-wire
    each node's next pointer to point backward instead of forward.  When the
    traversal ends, prev points to the new head.  No extra nodes or array
    copies are needed — the in-place pointer rewiring is only possible
    because a linked list's structure is explicit.
    Time: O(N)  Space: O(1)
    """
    prev = None
    current = ll._head
    while current is not None:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    ll._head = prev


# ---------------------------------------------------------------------------
# Algorithm 3: Merge Two Sorted Linked Lists
# ---------------------------------------------------------------------------

def merge_sorted(a: LinkedList, b: LinkedList) -> LinkedList:
    """
    Merge two ascending-sorted linked lists into a single sorted list.

    A dummy sentinel node anchors the result list so that head-insertion
    needs no special case.  At each step the smaller of the two current
    nodes is appended by re-linking its next pointer — no new Node objects
    are created.  This O(1)-space merge is only possible with linked lists;
    merging two sorted arrays always requires an auxiliary buffer of O(n+m).
    Time: O(N + M)  Space: O(1)
    """
    dummy = Node(None)
    tail = dummy

    cur_a = a._head
    cur_b = b._head

    while cur_a is not None and cur_b is not None:
        if cur_a.data <= cur_b.data:
            tail.next = cur_a
            cur_a = cur_a.next
        else:
            tail.next = cur_b
            cur_b = cur_b.next
        tail = tail.next

    tail.next = cur_a if cur_a is not None else cur_b

    result = LinkedList()
    result._head = dummy.next
    current = result._head
    count = 0
    while current is not None:
        count += 1
        current = current.next
    result._size = count
    return result


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _build(values: list) -> LinkedList:
    ll = LinkedList()
    for v in values:
        ll.insert(v)
    return ll


def separator(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Demo / main
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # ------------------------------------------------------------------
    # Demo 1: Floyd's Cycle Detection
    # ------------------------------------------------------------------
    separator("Algorithm 1: Floyd's Cycle Detection (Tortoise and Hare)")
    print("""
Description:
  Two pointers traverse the list simultaneously: a slow pointer that
  advances one node per step and a fast pointer that advances two.
  On an acyclic list the fast pointer reaches None and terminates.
  On a cyclic list the fast pointer eventually laps the slow one —
  they meet somewhere inside the loop.  A second phase resets the
  slow pointer to the head; advancing both one step at a time then
  guarantees convergence exactly at the cycle's entry node.  The
  algorithm is purely pointer-based: no visited-set or extra memory
  is needed, making it O(1) space.
  Time complexity: O(N)   Space complexity: O(1)
""")

    # Acyclic cases
    print("-- Acyclic lists --")
    for values in [[], [42], [1, 2, 3, 4, 5]]:
        ll = _build(values)
        print(f"  List {values!s:<20}  cycle={has_cycle(ll)}  entry={cycle_entry(ll)}")

    # Cyclic cases: inject a cycle then test
    print("\n-- Cyclic lists --")
    cycle_cases = [
        ([10, 20, 30, 40, 50], 0, "tail -> head (index 0)"),
        ([10, 20, 30, 40, 50], 2, "tail -> index 2 (value 30)"),
        ([10, 20, 30, 40, 50], 4, "tail -> last node (self-loop)"),
    ]
    for values, target, description in cycle_cases:
        ll = _build(values)
        print(f"\n  Before cycle: {_display_no_cycle(ll)}")
        _inject_cycle(ll, target)
        detected = has_cycle(ll)
        entry    = cycle_entry(ll)
        print(f"  Cycle wired:  {description}")
        print(f"  has_cycle()={detected}  cycle_entry()={entry}")

    # ------------------------------------------------------------------
    # Demo 2: In-Place Reversal
    # ------------------------------------------------------------------
    separator("Algorithm 2: In-Place Linked List Reversal")
    print("""
Description:
  Three local pointers (prev, current, nxt) traverse the list once.
  At each node, nxt saves the forward link before current.next is
  re-pointed backward to prev.  prev then advances to current, and
  current advances to nxt.  When current reaches None the loop ends
  and prev holds the new head.  Because only three pointer variables
  are used regardless of list length, auxiliary space is O(1) —
  impossible to achieve when reversing a contiguous array, which
  always needs at least a temporary swap variable per element or a
  full O(N) copy.
  Time complexity: O(N)   Space complexity: O(1)
""")

    reversal_cases = [
        [],
        [1],
        [1, 2],
        [1, 2, 3, 4, 5],
        ["apple", "banana", "cherry"],
    ]
    print(f"  {'Before':<40}  After")
    print("  " + "-" * 75)
    for values in reversal_cases:
        ll = _build(values)
        before = list(values)
        reverse(ll)
        after_elements = []
        cur = ll._head
        while cur:
            after_elements.append(cur.data)
            cur = cur.next
        before_str = str(before)
        after_str  = str(after_elements)
        print(f"  {before_str:<40}  {after_str}")

    # ------------------------------------------------------------------
    # Demo 3: Merge Two Sorted Linked Lists
    # ------------------------------------------------------------------
    separator("Algorithm 3: Merge Two Sorted Linked Lists")
    print("""
Description:
  A dummy sentinel node anchors the growing result list so that no
  special case is needed when inserting the very first element.  The
  algorithm walks both lists simultaneously, always appending the
  smaller of the two current nodes by re-linking its next pointer —
  zero new Node allocations.  This O(1)-space merge exploits the
  linked list's ability to splice nodes cheaply; merging sorted arrays
  always requires allocating an auxiliary buffer of O(N + M).  When
  one list is exhausted, the remainder of the other is attached in a
  single pointer assignment.
  Time complexity: O(N + M)   Space complexity: O(1) extra
""")

    merge_cases = [
        ([1, 3, 5, 7],    [2, 4, 6, 8]),
        ([1, 2, 3],       [4, 5, 6]),
        ([4, 5, 6],       [1, 2, 3]),
        ([1, 4, 7, 10],   [2, 3, 8, 9, 11, 12]),
        ([],              [1, 2, 3]),
        ([5],             [1, 2, 10]),
        ([1],             [1]),
    ]

    print(f"  {'List A':<28}  {'List B':<28}  Merged")
    print("  " + "-" * 85)
    for vals_a, vals_b in merge_cases:
        a = _build(vals_a)
        b = _build(vals_b)
        merged = merge_sorted(a, b)
        result_elements = []
        cur = merged._head
        while cur:
            result_elements.append(cur.data)
            cur = cur.next
        expected = sorted(vals_a + vals_b)
        status = "PASS" if result_elements == expected else "FAIL"
        print(f"  {str(vals_a):<28}  {str(vals_b):<28}  {result_elements}  [{status}]")
