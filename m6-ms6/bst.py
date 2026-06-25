"""
Binary Search Tree (BST) implementation with insert, search, delete,
and four traversal strategies: in-order, pre-order, post-order, level-order.

BST property: for every node N,
  all keys in N.left  < N.key
  all keys in N.right > N.key
"""


class Node:
    """
    Represents a single node in a Binary Search Tree.

    Each node stores one comparable key and maintains two child pointers:
      - left  : points to a child whose key is strictly less than this node's key
      - right : points to a child whose key is strictly greater than this node's key

    Leaf nodes have both pointers set to None.

    Attributes:
        key   : The value stored in this node (must support < and > comparisons).
        left  : Reference to the left child Node, or None.
        right : Reference to the right child Node, or None.
    """

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class binary_tree_search:
    """
    A Binary Search Tree (BST) with insert, search, delete, and four traversals.

    A BST is a rooted binary tree where every node satisfies the BST property:
      - All keys in the left subtree  are strictly less    than the node's key.
      - All keys in the right subtree are strictly greater than the node's key.

    This property lets insert, search, and delete all run in O(h) time, where h
    is the height of the tree.  For a balanced tree h = O(log n); in the worst
    case (sorted input) h = O(n).

    Supported operations:
      insert(key)      — add a key; duplicates are ignored
      search(key)      — return True/False
      delete(key)      — remove a key; no-op if absent
      inorder()        — keys in ascending order        (left → node → right)
      preorder()       — keys root-first                (node → left → right)
      postorder()      — keys leaves-first              (left → right → node)
      level_order()    — keys breadth-first by level

    Attributes:
        root : The root Node of the tree, or None if the tree is empty.
    """

    def __init__(self):
        self.root = None

    # -------------------------------------------------------------------------
    # Insert
    # -------------------------------------------------------------------------

    def insert(self, key):
        """Insert key into the BST. Duplicate keys are silently ignored."""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        """Recursively find the correct position and insert a new node."""
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        # equal key: duplicate — no action
        return node

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(self, key):
        """Return True if key exists in the BST, False otherwise."""
        return self._search(self.root, key)

    def _search(self, node, key):
        """Recursively traverse left or right based on key comparison."""
        if node is None:
            return False
        if key == node.key:
            return True
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    # -------------------------------------------------------------------------
    # Delete
    # -------------------------------------------------------------------------

    def delete(self, key):
        """Remove key from the BST. No-op if the key is not present."""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        """
        Recursively locate and remove the node with the given key.

        Three cases:
          1. Leaf node            — simply remove it.
          2. One child            — replace node with its only child.
          3. Two children         — replace node's key with its in-order
                                    successor (smallest key in right subtree),
                                    then delete that successor from the right subtree.
        """
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Case 1 & 2: zero or one child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Case 3: two children — use in-order successor
            successor = self._min_node(node.right)
            node.key = successor.key
            node.right = self._delete(node.right, successor.key)
        return node

    def _min_node(self, node):
        """Return the node with the smallest key in the subtree rooted at node."""
        while node.left is not None:
            node = node.left
        return node

    # -------------------------------------------------------------------------
    # Minimum / Maximum
    # -------------------------------------------------------------------------

    def find_min(self):
        """
        Return the minimum key in the BST, or None if the tree is empty.

        In a BST the minimum is always the leftmost node: follow left pointers
        until there is no left child.

        Time:  O(h)  — h is the tree height (O(log n) balanced, O(n) worst)
        Space: O(1)  — iterative, no call stack
        """
        if self.root is None:
            return None
        return self._min_node(self.root).key

    def find_max(self):
        """
        Return the maximum key in the BST, or None if the tree is empty.

        In a BST the maximum is always the rightmost node: follow right pointers
        until there is no right child.

        Time:  O(h)
        Space: O(1)
        """
        if self.root is None:
            return None
        node = self.root
        while node.right is not None:
            node = node.right
        return node.key

    # -------------------------------------------------------------------------
    # Height
    # -------------------------------------------------------------------------

    def height(self):
        """
        Return the height of the tree (number of edges on the longest root-to-leaf path).

        An empty tree has height -1; a single-node tree has height 0.

        Time:  O(n)  — every node is visited once
        Space: O(h)  — recursion stack depth equals tree height
        """
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    # -------------------------------------------------------------------------
    # BST Validation
    # -------------------------------------------------------------------------

    def is_valid_bst(self):
        """
        Return True if the tree satisfies the BST property for every node.

        Uses a min/max boundary approach: each recursive call narrows the
        valid key range, catching violations anywhere in the tree.

        Time:  O(n)
        Space: O(h)
        """
        return self._is_valid(self.root, float('-inf'), float('inf'))

    def _is_valid(self, node, min_val, max_val):
        if node is None:
            return True
        if not (min_val < node.key < max_val):
            return False
        return (self._is_valid(node.left, min_val, node.key) and
                self._is_valid(node.right, node.key, max_val))

    # -------------------------------------------------------------------------
    # Kth Smallest
    # -------------------------------------------------------------------------

    def find_kth_smallest(self, k):
        """
        Return the k-th smallest key (1-indexed), or None if k is out of range.

        Performs an in-order traversal and stops as soon as the k-th node is
        reached, so it avoids visiting the entire tree when k is small.

        Time:  O(h + k)
        Space: O(h)
        """
        self._kth_count = 0
        self._kth_result = None
        self._kth_inorder(self.root, k)
        return self._kth_result

    def _kth_inorder(self, node, k):
        if node is None or self._kth_result is not None:
            return
        self._kth_inorder(node.left, k)
        self._kth_count += 1
        if self._kth_count == k:
            self._kth_result = node.key
            return
        self._kth_inorder(node.right, k)

    # -------------------------------------------------------------------------
    # Balance Detection
    # -------------------------------------------------------------------------

    def is_balanced(self):
        """
        Return True if every node satisfies the AVL balance invariant:
        |height(left) - height(right)| <= 1.

        Uses a single post-order pass that returns both the subtree height and
        its balance status, avoiding redundant height recomputation.  As soon
        as one unbalanced node is found the rest of the traversal is skipped.

        Time:  O(n)
        Space: O(h)
        """
        balanced, _ = self._check_balance(self.root)
        return balanced

    def _check_balance(self, node):
        """
        Return (is_balanced, height) for the subtree rooted at node.

        Returns (False, -1) as a sentinel the moment any violation is found,
        short-circuiting further traversal up the call stack.
        """
        if node is None:
            return True, -1
        left_ok, left_h = self._check_balance(node.left)
        right_ok, right_h = self._check_balance(node.right)
        if not left_ok or not right_ok:
            return False, -1
        if abs(left_h - right_h) > 1:
            return False, -1
        return True, 1 + max(left_h, right_h)

    def node_balance_factor(self, key):
        """
        Return the balance factor (left_height - right_height) for the node
        with the given key, or None if the key is not present.

        Interpretation:
          0         perfectly balanced subtree heights
          +1 / -1   off by one (still AVL-valid)
          >= +2     left-heavy violation
          <= -2     right-heavy violation

        Time:  O(h) to locate the node + O(h) to compute heights = O(h)
        Space: O(h)
        """
        node = self._find_node(self.root, key)
        if node is None:
            return None
        return self._height(node.left) - self._height(node.right)

    def _find_node(self, node, key):
        """Return the Node with the given key, or None if absent."""
        if node is None:
            return None
        if key == node.key:
            return node
        if key < node.key:
            return self._find_node(node.left, key)
        return self._find_node(node.right, key)

    def balance_report(self):
        """
        Return a dict summarising the tree's balance characteristics.

        Keys
        ----
        is_balanced      : bool  — True when every node's |balance factor| <= 1
        tree_height      : int   — actual height (-1 for empty tree)
        node_count       : int   — total number of nodes
        ideal_height     : int   — floor(log2(n)), the minimum possible height
        height_ratio     : float — tree_height / ideal_height  (1.0 = optimal)
        unbalanced_nodes : list  — [(key, balance_factor), ...] for |bf| > 1
        max_imbalance    : int   — largest |balance_factor| found
        diagnosis        : str   — plain-English description

        Note: this method calls _height() once per node making it O(n^2) in
        the worst case.  Use is_balanced() for a hot-path O(n) check.

        Time:  O(n^2) worst case
        Space: O(h)
        """
        import math

        node_count = self._count_nodes(self.root)
        tree_height = self.height()

        if node_count == 0:
            return {
                "is_balanced": True,
                "tree_height": -1,
                "node_count": 0,
                "ideal_height": -1,
                "height_ratio": 1.0,
                "unbalanced_nodes": [],
                "max_imbalance": 0,
                "diagnosis": "Tree is empty.",
            }

        ideal_height = math.floor(math.log2(node_count))
        height_ratio = (tree_height / ideal_height) if ideal_height > 0 else 1.0

        unbalanced = []
        self._collect_unbalanced(self.root, unbalanced)
        max_imbalance = max((abs(bf) for _, bf in unbalanced), default=0)
        balanced = len(unbalanced) == 0

        if balanced:
            diagnosis = "Tree is balanced (every node's |balance factor| <= 1)."
        else:
            worst_key, worst_bf = max(unbalanced, key=lambda x: abs(x[1]))
            side = "left-heavy" if worst_bf > 0 else "right-heavy"
            diagnosis = (
                f"Tree is unbalanced. {len(unbalanced)} node(s) violate the AVL "
                f"invariant. Worst offender: node {worst_key} is {side} "
                f"(balance factor {worst_bf:+d})."
            )

        return {
            "is_balanced": balanced,
            "tree_height": tree_height,
            "node_count": node_count,
            "ideal_height": ideal_height,
            "height_ratio": round(height_ratio, 2),
            "unbalanced_nodes": unbalanced,
            "max_imbalance": max_imbalance,
            "diagnosis": diagnosis,
        }

    def _count_nodes(self, node):
        """Return the total number of nodes in the subtree rooted at node."""
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    def _collect_unbalanced(self, node, result):
        """Append (key, balance_factor) for every node whose |bf| > 1."""
        if node is None:
            return
        bf = self._height(node.left) - self._height(node.right)
        if abs(bf) > 1:
            result.append((node.key, bf))
        self._collect_unbalanced(node.left, result)
        self._collect_unbalanced(node.right, result)

    # -------------------------------------------------------------------------
    # Traversals
    # -------------------------------------------------------------------------

    def inorder(self):
        """
        Return keys in ascending order (left → node → right).
        Useful for verifying the BST property.

        Example (tree built from [50, 30, 70, 20, 40, 60, 80]):

                50
               /  \\
             30    70
            / \\  / \\
           20 40 60 80

        >>> bst.inorder()
        [20, 30, 40, 50, 60, 70, 80]
        """
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def preorder(self):
        """
        Return keys in pre-order (node → left → right).
        Useful for copying or serialising the tree structure.

        Example (tree built from [50, 30, 70, 20, 40, 60, 80]):

                50
               /  \\
             30    70
            / \\  / \\
           20 40 60 80

        >>> bst.preorder()
        [50, 30, 20, 40, 70, 60, 80]
        """
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.key)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        """
        Return keys in post-order (left → right → node).
        Useful for safely deleting the entire tree (children before parent).

        Example (tree built from [50, 30, 70, 20, 40, 60, 80]):

                50
               /  \\
             30    70
            / \\  / \\
           20 40 60 80

        >>> bst.postorder()
        [20, 40, 30, 60, 80, 70, 50]
        """
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.key)

    def level_order(self):
        """
        Return keys level by level (breadth-first, top → bottom, left → right).
        Uses a FIFO queue to process nodes one level at a time.
        """
        if self.root is None:
            return []
        result, queue = [], [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.key)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    # -------------------------------------------------------------------------
    # Visual Representation
    # -------------------------------------------------------------------------

    def print_tree(self, label=None):
        """
        Print an ASCII diagram of the BST to stdout.

        Optional label is printed as a header above the diagram.

        Example output for keys [50, 30, 70, 20, 40, 60, 80]:

              _50_
             /    \\
           _30    70_
          /   \\  /   \\
         20   40 60   80

        Time:  O(n)
        Space: O(n)  — stores one string per node across all levels
        """
        if label:
            print(f"\n{label}")
            print("-" * len(label))
        if self.root is None:
            print("(empty tree)")
            return
        lines, _, _, _ = self._display(self.root)
        for line in lines:
            print(line)

    def _display(self, node):
        """
        Recursively build ASCII lines for the subtree rooted at node.

        Returns (lines, width, height, middle) where:
          lines  — list of equal-length strings forming the diagram
          width  — character width of the widest line
          height — number of lines
          middle — column index of the root label's centre character
        """
        label = str(node.key)
        label_w = len(label)

        # Leaf node
        if node.left is None and node.right is None:
            return [label], label_w, 1, label_w // 2

        # Only right child
        if node.left is None:
            lines, n, p, x = self._display(node.right)
            first  = label + x * '_' + (n - x) * ' '
            second = label_w * ' ' + x * ' ' + '\\' + (n - x - 1) * ' '
            body   = [label_w * ' ' + ln for ln in lines]
            return [first, second] + body, n + label_w, p + 2, label_w // 2

        # Only left child
        if node.right is None:
            lines, n, p, x = self._display(node.left)
            first  = (x + 1) * ' ' + (n - x - 1) * '_' + label
            second = x * ' ' + '/' + (n - x - 1 + label_w) * ' '
            body   = [ln + label_w * ' ' for ln in lines]
            return [first, second] + body, n + label_w, p + 2, n + label_w // 2

        # Two children
        left_lines,  n, p, x = self._display(node.left)
        right_lines, m, q, y = self._display(node.right)
        first  = (x + 1) * ' ' + (n - x - 1) * '_' + label + y * '_' + (m - y) * ' '
        second = x * ' ' + '/' + (n - x - 1 + label_w + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left_lines  += [n * ' '] * (q - p)
        elif q < p:
            right_lines += [m * ' '] * (p - q)
        body = [a + label_w * ' ' + b for a, b in zip(left_lines, right_lines)]
        return [first, second] + body, n + m + label_w, max(p, q) + 2, n + label_w // 2


# -----------------------------------------------------------------------------
# Map — BST-backed key-value store
# -----------------------------------------------------------------------------

class MapNode:
    """Node storing a key-value pair for the Map BST."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class Map:
    """
    An ordered map backed by a Binary Search Tree.

    Keys must be comparable (support < and >).  Values can be any object.
    BST ordering on keys gives O(h) put/get/delete and O(n) sorted iteration,
    where h is the tree height (O(log n) balanced, O(n) worst-case).

    Operations:
      put(key, value)        — insert or overwrite
      get(key)               — return value; raises KeyError if absent
      get_or_default(key, d) — return value, or d if key is absent
      delete(key)            — remove entry; no-op if key absent
      contains_key(key)      — True/False membership test
      keys()                 — all keys in ascending order
      values()               — values in key-ascending order
      items()                — (key, value) pairs in key-ascending order
      size()                 — number of entries

    Python protocols: __len__, __contains__, __getitem__, __setitem__,
                      __delitem__, __iter__, __repr__.
    """

    def __init__(self):
        self._root = None
        self._size = 0

    # -------------------------------------------------------------------------
    # Put / Get / Delete
    # -------------------------------------------------------------------------

    def put(self, key, value):
        """Insert key-value pair, or overwrite value if key already exists."""
        self._root, inserted = self._put(self._root, key, value)
        if inserted:
            self._size += 1

    def _put(self, node, key, value):
        if node is None:
            return MapNode(key, value), True
        if key < node.key:
            node.left, inserted = self._put(node.left, key, value)
        elif key > node.key:
            node.right, inserted = self._put(node.right, key, value)
        else:
            node.value = value   # overwrite existing entry
            inserted = False
        return node, inserted

    def get(self, key):
        """Return the value for key. Raises KeyError if key is absent."""
        node = self._find(self._root, key)
        if node is None:
            raise KeyError(key)
        return node.value

    def get_or_default(self, key, default=None):
        """Return value for key, or default if key is absent."""
        node = self._find(self._root, key)
        return node.value if node is not None else default

    def contains_key(self, key):
        """Return True if key exists in the map."""
        return self._find(self._root, key) is not None

    def delete(self, key):
        """Remove the entry for key. No-op if key is not present."""
        self._root, deleted = self._delete(self._root, key)
        if deleted:
            self._size -= 1

    def _delete(self, node, key):
        if node is None:
            return None, False
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
        elif key > node.key:
            node.right, deleted = self._delete(node.right, key)
        else:
            deleted = True
            if node.left is None:
                return node.right, deleted
            if node.right is None:
                return node.left, deleted
            # Two children: replace with in-order successor (smallest in right subtree)
            successor = self._min_node(node.right)
            node.key, node.value = successor.key, successor.value
            node.right, _ = self._delete(node.right, successor.key)
        return node, deleted

    def size(self):
        """Return the number of entries in the map."""
        return self._size

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _find(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node
        if key < node.key:
            return self._find(node.left, key)
        return self._find(node.right, key)

    def _min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def _inorder_collect(self, node, result, extract):
        if node:
            self._inorder_collect(node.left, result, extract)
            result.append(extract(node))
            self._inorder_collect(node.right, result, extract)

    # -------------------------------------------------------------------------
    # Sorted views
    # -------------------------------------------------------------------------

    def keys(self):
        """Return all keys in ascending order."""
        result = []
        self._inorder_collect(self._root, result, lambda n: n.key)
        return result

    def values(self):
        """Return all values in key-ascending order."""
        result = []
        self._inorder_collect(self._root, result, lambda n: n.value)
        return result

    def items(self):
        """Return all (key, value) pairs in key-ascending order."""
        result = []
        self._inorder_collect(self._root, result, lambda n: (n.key, n.value))
        return result

    # -------------------------------------------------------------------------
    # Python protocols
    # -------------------------------------------------------------------------

    def __len__(self):
        return self._size

    def __contains__(self, key):
        return self.contains_key(key)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        if not self.contains_key(key):
            raise KeyError(key)
        self.delete(key)

    def __iter__(self):
        return iter(self.keys())

    def __repr__(self):
        pairs = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"Map({{{pairs}}})"


# -----------------------------------------------------------------------------
# Demo
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("INSERTION — step-by-step visual")
    print("=" * 60)
    bst = binary_tree_search()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(val)
        bst.print_tree(f"After inserting {val}")

    print("\nTraversals:")
    print("Inorder:    ", bst.inorder())      # [20, 30, 40, 50, 60, 70, 80]
    print("Preorder:   ", bst.preorder())     # [50, 30, 20, 40, 70, 60, 80]
    print("Postorder:  ", bst.postorder())    # [20, 40, 30, 60, 80, 70, 50]
    print("Level-order:", bst.level_order())  # [50, 30, 70, 20, 40, 60, 80]

    print("\nSearch 40:", bst.search(40))   # True
    print("Search 99:", bst.search(99))    # False

    # --- Min / Max ---
    print("\nMinimum:", bst.find_min())     # 20
    print("Maximum:", bst.find_max())      # 80

    # --- Height ---
    print("Height: ", bst.height())        # 2  (root→30→20 or root→70→80)

    # --- BST Validation ---
    print("Valid BST:", bst.is_valid_bst())  # True

    # --- Kth Smallest ---
    print("1st smallest:", bst.find_kth_smallest(1))  # 20
    print("3rd smallest:", bst.find_kth_smallest(3))  # 40
    print("7th smallest:", bst.find_kth_smallest(7))  # 80
    print("8th smallest:", bst.find_kth_smallest(8))  # None (out of range)

    print("\n" + "=" * 60)
    print("DELETION — step-by-step visual")
    print("=" * 60)

    bst.print_tree("Before any deletions")

    bst.delete(30)  # node with two children — replaced by in-order successor 40
    bst.print_tree("After deleting 30 (node with two children → successor 40 takes its place)")
    print("Inorder:", bst.inorder())       # [20, 40, 50, 60, 70, 80]
    print("Min:", bst.find_min())          # 20
    print("Max:", bst.find_max())          # 80

    bst.delete(20)  # leaf node
    bst.print_tree("After deleting 20 (leaf node)")
    print("Inorder:", bst.inorder())       # [40, 50, 60, 70, 80]
    print("Min:", bst.find_min())          # 40

    bst.delete(70)  # node with one child (60 and 80 → 60 is left child, 80 is right)
    bst.print_tree("After deleting 70 (node with two children → successor 80 takes its place)")
    print("Inorder:", bst.inorder())

    # -------------------------------------------------------------------------
    # Balance Detection Demo
    # -------------------------------------------------------------------------

    print("\n" + "=" * 60)
    print("BALANCE DETECTION")
    print("=" * 60)

    # --- Balanced tree: complete structure ---
    balanced_bst = binary_tree_search()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        balanced_bst.insert(val)

    balanced_bst.print_tree("[Balanced tree]")
    print("is_balanced():", balanced_bst.is_balanced())                   # True
    print("node_balance_factor(50):", balanced_bst.node_balance_factor(50))  # 0
    print("node_balance_factor(30):", balanced_bst.node_balance_factor(30))  # 0
    report = balanced_bst.balance_report()
    print("balance_report():")
    for k, v in report.items():
        print(f"  {k:<20}: {v}")

    # --- Unbalanced tree: sorted insertion creates a right-skewed chain ---
    skewed_bst = binary_tree_search()
    for val in [10, 20, 30, 40, 50]:
        skewed_bst.insert(val)

    skewed_bst.print_tree("[Skewed tree] (sorted insertion → right-skewed chain)")
    print("is_balanced():", skewed_bst.is_balanced())                     # False
    print("node_balance_factor(10):", skewed_bst.node_balance_factor(10))  # -4
    print("node_balance_factor(20):", skewed_bst.node_balance_factor(20))  # -3
    report = skewed_bst.balance_report()
    print("balance_report():")
    for k, v in report.items():
        print(f"  {k:<20}: {v}")

    # --- node_balance_factor for a missing key ---
    print("\nnode_balance_factor(99):", skewed_bst.node_balance_factor(99))  # None

    # -------------------------------------------------------------------------
    # Map Demo
    # -------------------------------------------------------------------------

    print("\n" + "=" * 60)
    print("MAP (BST-backed key-value store)")
    print("=" * 60)

    m = Map()
    m.put("banana", 3)
    m.put("apple", 10)
    m.put("cherry", 7)
    m.put("date", 1)
    m["elderberry"] = 5      # __setitem__

    print("\nSize:", len(m))                        # 5
    print("Keys (sorted):", m.keys())              # ['apple','banana','cherry','date','elderberry']
    print("Values:       ", m.values())
    print("Items:        ", m.items())
    print("repr:         ", m)

    print("\nget('apple'):", m.get("apple"))        # 10
    print("m['cherry']:  ", m["cherry"])            # 7
    print("contains 'date':", "date" in m)          # True
    print("contains 'fig': ", "fig" in m)           # False

    print("\nOverwrite 'apple' → 99")
    m["apple"] = 99
    print("m['apple']:", m["apple"])               # 99

    print("\nget_or_default('fig', 0):", m.get_or_default("fig", 0))  # 0

    print("\nDelete 'banana'")
    del m["banana"]
    print("Size:", len(m))                         # 4
    print("Keys:", m.keys())

    print("\nIterate (for key in m):")
    for key in m:
        print(f"  {key}: {m[key]}")
