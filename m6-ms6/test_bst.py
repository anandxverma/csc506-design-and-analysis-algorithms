"""
Test suite for binary_tree_search.py

Covers: insert, search, delete, inorder, preorder, postorder, level_order,
        find_min, find_max, height, is_valid_bst, find_kth_smallest,
        is_balanced, node_balance_factor, balance_report.

Data sets used
--------------
  integers  : 25 values spanning negative, zero, and large positives
  floats    : 15 values including near-zero and large decimals
  strings   : 15 lowercase words
  Total unique items inserted across all data sets: 55
"""

import unittest
from bst import binary_tree_search


# ---------------------------------------------------------------------------
# Shared data sets (defined at module level so every test class can reuse them)
# ---------------------------------------------------------------------------

INTEGER_ITEMS = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35,
                 45, 55, 65, 75, 90, -5, -20, 0, 100, 200,
                 150, 175, 125, 85, 95]

FLOAT_ITEMS = [3.14, 2.71, 1.41, 0.57, 9.81,
               1.73, 2.23, 0.01, 100.5, 50.25,
               75.75, 25.1, 12.6, 88.8, 0.001]

STRING_ITEMS = ["mango", "apple", "orange", "banana", "grape",
                "kiwi", "peach", "plum", "cherry", "fig",
                "lemon", "lime", "melon", "papaya", "guava"]


def build_bst(items):
    """Return a fresh BST pre-loaded with the given items."""
    bst = binary_tree_search()
    for item in items:
        bst.insert(item)
    return bst


# ===========================================================================
# 1. Integer BST tests
# ===========================================================================

class TestIntegerBST(unittest.TestCase):
    """Tests using 25 integer keys."""

    def setUp(self):
        self.bst = build_bst(INTEGER_ITEMS)

    # --- insert / search ---

    def test_insert_all_items_found(self):
        for item in INTEGER_ITEMS:
            self.assertTrue(self.bst.search(item), f"Expected {item} to be in BST")

    def test_search_absent_key(self):
        for absent in [999, -999, 1000, 42]:
            self.assertFalse(self.bst.search(absent))

    def test_duplicate_insert_ignored(self):
        bst = build_bst([10, 20, 30])
        bst.insert(20)
        self.assertEqual(bst.inorder(), [10, 20, 30])

    # --- inorder produces sorted output ---

    def test_inorder_sorted(self):
        result = self.bst.inorder()
        self.assertEqual(result, sorted(INTEGER_ITEMS))

    def test_inorder_count(self):
        self.assertEqual(len(self.bst.inorder()), len(set(INTEGER_ITEMS)))

    # --- preorder / postorder / level_order basic sanity ---

    def test_preorder_contains_all(self):
        self.assertEqual(sorted(self.bst.preorder()), sorted(INTEGER_ITEMS))

    def test_postorder_contains_all(self):
        self.assertEqual(sorted(self.bst.postorder()), sorted(INTEGER_ITEMS))

    def test_level_order_contains_all(self):
        self.assertEqual(sorted(self.bst.level_order()), sorted(INTEGER_ITEMS))

    def test_preorder_root_first(self):
        # The first key inserted (50) becomes the root.
        self.assertEqual(self.bst.preorder()[0], 50)

    def test_postorder_root_last(self):
        self.assertEqual(self.bst.postorder()[-1], 50)

    def test_level_order_root_first(self):
        self.assertEqual(self.bst.level_order()[0], 50)

    # --- min / max ---

    def test_find_min(self):
        self.assertEqual(self.bst.find_min(), min(INTEGER_ITEMS))

    def test_find_max(self):
        self.assertEqual(self.bst.find_max(), max(INTEGER_ITEMS))

    # --- height ---

    def test_height_positive(self):
        self.assertGreater(self.bst.height(), 0)

    def test_height_lower_bound(self):
        import math
        n = len(set(INTEGER_ITEMS))
        self.assertGreaterEqual(self.bst.height(), math.floor(math.log2(n)))

    # --- is_valid_bst ---

    def test_valid_bst_after_inserts(self):
        self.assertTrue(self.bst.is_valid_bst())

    # --- find_kth_smallest ---

    def test_kth_smallest_first(self):
        self.assertEqual(self.bst.find_kth_smallest(1), min(INTEGER_ITEMS))

    def test_kth_smallest_last(self):
        n = len(set(INTEGER_ITEMS))
        self.assertEqual(self.bst.find_kth_smallest(n), max(INTEGER_ITEMS))

    def test_kth_smallest_middle(self):
        sorted_items = sorted(set(INTEGER_ITEMS))
        for k in [3, 7, 12, 18]:
            self.assertEqual(self.bst.find_kth_smallest(k), sorted_items[k - 1])

    def test_kth_smallest_out_of_range(self):
        n = len(set(INTEGER_ITEMS))
        self.assertIsNone(self.bst.find_kth_smallest(n + 1))
        self.assertIsNone(self.bst.find_kth_smallest(0))

    # --- delete ---

    def test_delete_leaf(self):
        self.bst.delete(-20)  # leaf (leftmost)
        self.assertFalse(self.bst.search(-20))
        self.assertTrue(self.bst.is_valid_bst())

    def test_delete_node_one_child(self):
        # Insert 5 so that 10 has a right child (5 < 10, left of 10)
        bst = build_bst([50, 30, 10, 5])
        bst.delete(10)  # 10 has one child (5)
        self.assertFalse(bst.search(10))
        self.assertTrue(bst.search(5))
        self.assertTrue(bst.is_valid_bst())

    def test_delete_node_two_children(self):
        self.bst.delete(30)  # has left=20 and right=40
        self.assertFalse(self.bst.search(30))
        self.assertTrue(self.bst.is_valid_bst())

    def test_delete_root(self):
        self.bst.delete(50)
        self.assertFalse(self.bst.search(50))
        self.assertTrue(self.bst.is_valid_bst())

    def test_delete_absent_key_no_error(self):
        before = self.bst.inorder()
        self.bst.delete(9999)
        self.assertEqual(self.bst.inorder(), before)

    def test_delete_restores_sorted_inorder(self):
        for val in [10, 90, 50]:
            self.bst.delete(val)
        remaining = sorted(v for v in set(INTEGER_ITEMS) if v not in (10, 90, 50))
        self.assertEqual(self.bst.inorder(), remaining)

    # --- balance detection ---

    def test_balance_report_node_count(self):
        report = self.bst.balance_report()
        self.assertEqual(report["node_count"], len(set(INTEGER_ITEMS)))

    def test_node_balance_factor_root(self):
        bf = self.bst.node_balance_factor(50)
        self.assertIsNotNone(bf)

    def test_node_balance_factor_absent(self):
        self.assertIsNone(self.bst.node_balance_factor(9999))


# ===========================================================================
# 2. Float BST tests
# ===========================================================================

class TestFloatBST(unittest.TestCase):
    """Tests using 15 float keys."""

    def setUp(self):
        self.bst = build_bst(FLOAT_ITEMS)

    def test_all_floats_inserted(self):
        for item in FLOAT_ITEMS:
            self.assertTrue(self.bst.search(item))

    def test_inorder_sorted(self):
        self.assertEqual(self.bst.inorder(), sorted(FLOAT_ITEMS))

    def test_find_min_float(self):
        self.assertAlmostEqual(self.bst.find_min(), min(FLOAT_ITEMS))

    def test_find_max_float(self):
        self.assertAlmostEqual(self.bst.find_max(), max(FLOAT_ITEMS))

    def test_valid_bst_floats(self):
        self.assertTrue(self.bst.is_valid_bst())

    def test_kth_smallest_float(self):
        sorted_items = sorted(FLOAT_ITEMS)
        self.assertAlmostEqual(self.bst.find_kth_smallest(5), sorted_items[4])

    def test_delete_float(self):
        self.bst.delete(3.14)
        self.assertFalse(self.bst.search(3.14))
        self.assertTrue(self.bst.is_valid_bst())

    def test_preorder_postorder_same_set(self):
        self.assertEqual(sorted(self.bst.preorder()), sorted(self.bst.postorder()))

    def test_balance_report_floats(self):
        report = self.bst.balance_report()
        self.assertEqual(report["node_count"], len(FLOAT_ITEMS))
        self.assertIn("diagnosis", report)


# ===========================================================================
# 3. String BST tests
# ===========================================================================

class TestStringBST(unittest.TestCase):
    """Tests using 15 lowercase string keys (lexicographic ordering)."""

    def setUp(self):
        self.bst = build_bst(STRING_ITEMS)

    def test_all_strings_inserted(self):
        for item in STRING_ITEMS:
            self.assertTrue(self.bst.search(item))

    def test_search_absent_string(self):
        self.assertFalse(self.bst.search("watermelon"))
        self.assertFalse(self.bst.search("MANGO"))   # case-sensitive

    def test_inorder_lexicographic(self):
        self.assertEqual(self.bst.inorder(), sorted(STRING_ITEMS))

    def test_find_min_string(self):
        self.assertEqual(self.bst.find_min(), min(STRING_ITEMS))

    def test_find_max_string(self):
        self.assertEqual(self.bst.find_max(), max(STRING_ITEMS))

    def test_kth_smallest_string(self):
        sorted_items = sorted(STRING_ITEMS)
        self.assertEqual(self.bst.find_kth_smallest(1), sorted_items[0])
        self.assertEqual(self.bst.find_kth_smallest(len(STRING_ITEMS)), sorted_items[-1])

    def test_delete_string(self):
        self.bst.delete("mango")
        self.assertFalse(self.bst.search("mango"))
        self.assertEqual(self.bst.inorder(), sorted(s for s in STRING_ITEMS if s != "mango"))

    def test_level_order_strings(self):
        lo = self.bst.level_order()
        self.assertEqual(sorted(lo), sorted(STRING_ITEMS))


# ===========================================================================
# 4. Edge-case / boundary tests
# ===========================================================================

class TestEdgeCases(unittest.TestCase):
    """Boundary conditions: empty tree, single node, skewed trees."""

    # --- empty tree ---

    def test_empty_search(self):
        bst = binary_tree_search()
        self.assertFalse(bst.search(1))

    def test_empty_inorder(self):
        self.assertEqual(binary_tree_search().inorder(), [])

    def test_empty_preorder(self):
        self.assertEqual(binary_tree_search().preorder(), [])

    def test_empty_postorder(self):
        self.assertEqual(binary_tree_search().postorder(), [])

    def test_empty_level_order(self):
        self.assertEqual(binary_tree_search().level_order(), [])

    def test_empty_find_min(self):
        self.assertIsNone(binary_tree_search().find_min())

    def test_empty_find_max(self):
        self.assertIsNone(binary_tree_search().find_max())

    def test_empty_height(self):
        self.assertEqual(binary_tree_search().height(), -1)

    def test_empty_is_valid_bst(self):
        self.assertTrue(binary_tree_search().is_valid_bst())

    def test_empty_kth_smallest(self):
        self.assertIsNone(binary_tree_search().find_kth_smallest(1))

    def test_empty_is_balanced(self):
        self.assertTrue(binary_tree_search().is_balanced())

    def test_empty_balance_report(self):
        report = binary_tree_search().balance_report()
        self.assertEqual(report["node_count"], 0)
        self.assertEqual(report["tree_height"], -1)

    # --- single node ---

    def test_single_node_search(self):
        bst = build_bst([42])
        self.assertTrue(bst.search(42))
        self.assertFalse(bst.search(0))

    def test_single_node_inorder(self):
        self.assertEqual(build_bst([42]).inorder(), [42])

    def test_single_node_height(self):
        self.assertEqual(build_bst([42]).height(), 0)

    def test_single_node_min_max(self):
        bst = build_bst([42])
        self.assertEqual(bst.find_min(), 42)
        self.assertEqual(bst.find_max(), 42)

    def test_single_node_is_balanced(self):
        self.assertTrue(build_bst([42]).is_balanced())

    def test_single_node_delete(self):
        bst = build_bst([42])
        bst.delete(42)
        self.assertEqual(bst.inorder(), [])
        self.assertIsNone(bst.find_min())

    # --- right-skewed tree (sorted ascending inserts) ---

    def test_skewed_right_is_unbalanced(self):
        bst = build_bst([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertFalse(bst.is_balanced())

    def test_skewed_right_height(self):
        bst = build_bst([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(bst.height(), 9)  # degenerate chain

    def test_skewed_right_valid_bst(self):
        bst = build_bst([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertTrue(bst.is_valid_bst())

    def test_skewed_right_inorder_sorted(self):
        items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(build_bst(items).inorder(), items)

    # --- left-skewed tree (sorted descending inserts) ---

    def test_skewed_left_is_unbalanced(self):
        bst = build_bst([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
        self.assertFalse(bst.is_balanced())

    def test_skewed_left_inorder_sorted(self):
        self.assertEqual(build_bst([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]).inorder(),
                         list(range(1, 11)))

    # --- perfectly balanced tree ---

    def test_balanced_tree_is_balanced(self):
        bst = build_bst([50, 30, 70, 20, 40, 60, 80])
        self.assertTrue(bst.is_balanced())

    def test_balanced_tree_height(self):
        bst = build_bst([50, 30, 70, 20, 40, 60, 80])
        self.assertEqual(bst.height(), 2)

    # --- balance report fields ---

    def test_balance_report_keys_present(self):
        bst = build_bst([50, 30, 70])
        report = bst.balance_report()
        for key in ("is_balanced", "tree_height", "node_count", "ideal_height",
                    "height_ratio", "unbalanced_nodes", "max_imbalance", "diagnosis"):
            self.assertIn(key, report)

    def test_balance_report_skewed_has_unbalanced_nodes(self):
        bst = build_bst([1, 2, 3, 4, 5])
        report = bst.balance_report()
        self.assertFalse(report["is_balanced"])
        self.assertGreater(len(report["unbalanced_nodes"]), 0)

    # --- node_balance_factor ---

    def test_balance_factor_leaf(self):
        bst = build_bst([50, 30, 70])
        self.assertEqual(bst.node_balance_factor(30), 0)
        self.assertEqual(bst.node_balance_factor(70), 0)

    def test_balance_factor_root_balanced(self):
        bst = build_bst([50, 30, 70, 20, 40, 60, 80])
        self.assertEqual(bst.node_balance_factor(50), 0)

    def test_balance_factor_skewed_root(self):
        bst = build_bst([10, 20, 30, 40, 50])
        bf = bst.node_balance_factor(10)
        self.assertLessEqual(bf, -2)   # right-heavy violation

    def test_balance_factor_missing_key_none(self):
        bst = build_bst([10, 20])
        self.assertIsNone(bst.node_balance_factor(99))


# ===========================================================================
# 5. Traversal relationship tests
# ===========================================================================

class TestTraversalRelationships(unittest.TestCase):
    """Verify structural relationships between traversal orders."""

    def setUp(self):
        # Use a well-known complete BST for predictable traversal results.
        self.bst = build_bst([50, 30, 70, 20, 40, 60, 80])

    def test_inorder_is_sorted(self):
        r = self.bst.inorder()
        self.assertEqual(r, sorted(r))

    def test_all_traversals_same_set(self):
        keys = {20, 30, 40, 50, 60, 70, 80}
        self.assertEqual(set(self.bst.inorder()), keys)
        self.assertEqual(set(self.bst.preorder()), keys)
        self.assertEqual(set(self.bst.postorder()), keys)
        self.assertEqual(set(self.bst.level_order()), keys)

    def test_preorder_root_first(self):
        self.assertEqual(self.bst.preorder()[0], 50)

    def test_postorder_root_last(self):
        self.assertEqual(self.bst.postorder()[-1], 50)

    def test_level_order_first_level(self):
        lo = self.bst.level_order()
        self.assertEqual(lo[0], 50)
        self.assertIn(lo[1], {30, 70})
        self.assertIn(lo[2], {30, 70})

    def test_inorder_large_dataset(self):
        bst = build_bst(INTEGER_ITEMS + FLOAT_ITEMS)
        result = bst.inorder()
        self.assertEqual(result, sorted(set(INTEGER_ITEMS + FLOAT_ITEMS)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
