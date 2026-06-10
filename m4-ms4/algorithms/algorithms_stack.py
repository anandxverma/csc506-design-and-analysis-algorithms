"""
Stack-based algorithms — three classic problems where LIFO ordering is essential.

Imports the Stack class from stack.py in the same package.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from stack import Stack


# ---------------------------------------------------------------------------
# Algorithm 1: Balanced Bracket Validator
# ---------------------------------------------------------------------------

_OPEN  = set("([{")
_CLOSE = set(")]}")
_MATCH = {')': '(', ']': '[', '}': '{'}


def is_balanced(expression: str) -> tuple[bool, str]:
    """
    Determine whether every opening bracket in `expression` is closed in the
    correct order.

    A stack is the natural fit: push each opening bracket, then on each
    closing bracket verify that the top of the stack holds its partner.
    Any mismatch or leftover item signals an error.
    Time: O(N)  Space: O(N)

    Returns (True, "") on success or (False, reason) on failure.
    """
    s = Stack()
    for i, ch in enumerate(expression):
        if ch in _OPEN:
            s.push((ch, i))
        elif ch in _CLOSE:
            if s.is_empty():
                return False, f"Unmatched '{ch}' at position {i}"
            top, pos = s.pop()
            if top != _MATCH[ch]:
                return False, (
                    f"Mismatched '{top}' at position {pos} "
                    f"closed by '{ch}' at position {i}"
                )
    if not s.is_empty():
        ch, pos = s.pop()
        return False, f"Unclosed '{ch}' at position {pos}"
    return True, ""


# ---------------------------------------------------------------------------
# Algorithm 2: Infix → Postfix (Shunting-Yard) + Postfix Evaluator
# ---------------------------------------------------------------------------

_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
_RIGHT_ASSOC = {'^'}


def infix_to_postfix(expression: str) -> list[str]:
    """
    Convert a tokenised infix expression to Reverse Polish Notation (postfix)
    using Dijkstra's Shunting-Yard algorithm.

    The operator stack enforces precedence and associativity: a lower- (or
    equal-) precedence operator arriving at the stack triggers a flush of
    higher-priority operators to the output before the new one is pushed.
    Parentheses act as temporary precedence barriers.
    Time: O(N)  Space: O(N)

    `expression` is a string of single-character tokens separated by spaces,
    e.g. "3 + 4 * 2" or "( 1 + 2 ) ^ 3".
    Returns the postfix token list, e.g. ['3', '4', '2', '*', '+'].
    """
    tokens = expression.split()
    output = []
    ops = Stack()

    for tok in tokens:
        if tok.lstrip('-').replace('.', '', 1).isdigit():
            output.append(tok)
        elif tok in _PRECEDENCE:
            while (
                not ops.is_empty()
                and ops.peek() in _PRECEDENCE
                and (
                    _PRECEDENCE[ops.peek()] > _PRECEDENCE[tok]
                    or (
                        _PRECEDENCE[ops.peek()] == _PRECEDENCE[tok]
                        and tok not in _RIGHT_ASSOC
                    )
                )
            ):
                output.append(ops.pop())
            ops.push(tok)
        elif tok == '(':
            ops.push(tok)
        elif tok == ')':
            while not ops.is_empty() and ops.peek() != '(':
                output.append(ops.pop())
            if ops.is_empty():
                raise ValueError("Mismatched parentheses")
            ops.pop()  # discard '('
        else:
            raise ValueError(f"Unknown token: {tok!r}")

    while not ops.is_empty():
        op = ops.pop()
        if op == '(':
            raise ValueError("Mismatched parentheses")
        output.append(op)

    return output


def evaluate_postfix(tokens: list[str]) -> float:
    """
    Evaluate a postfix (RPN) token list and return the numeric result.

    Each operand is pushed; each operator pops two operands, applies the
    operation, and pushes the result.  The final value on the stack is the
    answer.  The LIFO property ensures operands are consumed in the correct
    order relative to their operator.
    Time: O(N)  Space: O(N)
    """
    s = Stack()
    for tok in tokens:
        if tok.lstrip('-').replace('.', '', 1).isdigit():
            s.push(float(tok))
        else:
            b = s.pop()
            a = s.pop()
            if tok == '+':
                s.push(a + b)
            elif tok == '-':
                s.push(a - b)
            elif tok == '*':
                s.push(a * b)
            elif tok == '/':
                if b == 0:
                    raise ZeroDivisionError("Division by zero in expression")
                s.push(a / b)
            elif tok == '^':
                s.push(a ** b)
    return s.pop()


# ---------------------------------------------------------------------------
# Algorithm 3: Iterative Depth-First Search (DFS)
# ---------------------------------------------------------------------------

def dfs(graph: dict, start: str) -> list[str]:
    """
    Visit every reachable vertex using iterative DFS driven by an explicit
    stack.

    Unlike BFS (which uses a queue for level-order exploration), a stack
    causes DFS to dive as deep as possible along each path before backtracking.
    The iterative form avoids Python's recursion limit on large graphs.
    Time: O(V + E)  Space: O(V)
    """
    visited = set()
    order = []
    s = Stack()
    s.push(start)

    while not s.is_empty():
        vertex = s.pop()
        if vertex in visited:
            continue
        visited.add(vertex)
        order.append(vertex)
        # Push neighbours in reverse so the first neighbour is processed first
        for neighbor in reversed(graph.get(vertex, [])):
            if neighbor not in visited:
                s.push(neighbor)

    return order


def dfs_path(graph: dict, start: str, goal: str) -> list[str] | None:
    """
    Return *a* path from start to goal found via iterative DFS.
    Not guaranteed to be the shortest; returns None if no path exists.
    """
    if start == goal:
        return [start]

    visited = set()
    s = Stack()
    s.push((start, [start]))

    while not s.is_empty():
        vertex, path = s.pop()
        if vertex in visited:
            continue
        visited.add(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor == goal:
                return path + [neighbor]
            if neighbor not in visited:
                s.push((neighbor, path + [neighbor]))

    return None


# ---------------------------------------------------------------------------
# Demo / main
# ---------------------------------------------------------------------------

def separator(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


if __name__ == "__main__":

    # ------------------------------------------------------------------
    # Demo 1: Balanced Bracket Validator
    # ------------------------------------------------------------------
    separator("Algorithm 1: Balanced Bracket Validator")
    print("""
Description:
  A stack checks whether every opening bracket '(', '[', or '{' in an
  expression is closed by the correct partner in the correct order.
  Opening brackets are pushed; each closing bracket pops the stack and
  verifies a match.  Any mismatch, extra closing bracket, or unclosed
  opener is an error.  The LIFO property naturally enforces nesting:
  the most recently opened bracket must always be the next one closed.
  Time complexity: O(N)
""")

    test_cases = [
        ("(a + b) * [c - {d / e}]",  True),
        ("{[()]}",                    True),
        ("(((",                       False),
        ("([)]",                      False),
        (")()",                       False),
        ("int main() { return 0; }",  True),
    ]

    print(f"{'Expression':<40}  {'Valid?':<7}  Details")
    print("-" * 70)
    for expr, expected in test_cases:
        ok, reason = is_balanced(expr)
        status = "PASS" if ok == expected else "FAIL"
        detail = reason if not ok else "all brackets matched"
        print(f"  {expr!r:<38}  {'Yes' if ok else 'No':<7}  {detail}  [{status}]")

    # ------------------------------------------------------------------
    # Demo 2: Infix → Postfix + Evaluation
    # ------------------------------------------------------------------
    separator("Algorithm 2: Infix to Postfix (Shunting-Yard) + Evaluator")
    print("""
Description:
  The Shunting-Yard algorithm converts a human-readable infix expression
  such as "3 + 4 * 2" into Reverse Polish Notation (postfix) "3 4 2 * +"
  using an operator stack to enforce precedence and associativity rules.
  A second stack-based pass then evaluates the postfix form: operands are
  pushed and each operator pops two operands, computes the result, and
  pushes it back.  Both passes are O(N) with O(N) space.
""")

    expressions = [
        "3 + 4 * 2",
        "( 3 + 4 ) * 2",
        "2 ^ 3 ^ 2",
        "10 - 3 - 2",
        "( 1 + 2 ) * ( 3 + 4 ) / 7",
        "100 / 10 / 2",
    ]

    print(f"  {'Infix':<30}  {'Postfix':<30}  Result")
    print("  " + "-" * 72)
    for expr in expressions:
        postfix = infix_to_postfix(expr)
        result  = evaluate_postfix(postfix)
        postfix_str = " ".join(postfix)
        result_str  = f"{result:.4g}"
        print(f"  {expr:<30}  {postfix_str:<30}  {result_str}")

    # ------------------------------------------------------------------
    # Demo 3: Iterative DFS
    # ------------------------------------------------------------------
    separator("Algorithm 3: Iterative Depth-First Search (DFS)")
    print("""
Description:
  DFS explores a graph by diving as deep as possible down each path
  before backtracking.  Replacing the recursion call stack with an
  explicit LIFO stack makes the iterative version memory-safe on deep
  graphs.  Neighbours are pushed in reverse order so that the first
  listed neighbour is explored first — mirroring recursive DFS behaviour.
  Compared to BFS (which uses a queue), DFS tends to find a path quickly
  but does not guarantee the shortest one.
  Time complexity: O(V + E)
""")

    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E'],
    }

    print("Graph adjacency list (same graph used for BFS in queue_algorithms.py):")
    for v, nbrs in graph.items():
        print(f"  {v} -> {nbrs}")

    traversal = dfs(graph, 'A')
    print(f"\nDFS traversal from 'A':  {traversal}")

    path = dfs_path(graph, 'A', 'F')
    print(f"DFS path from 'A' to 'F': {' -> '.join(path)}")

    path2 = dfs_path(graph, 'D', 'C')
    print(f"DFS path from 'D' to 'C': {' -> '.join(path2)}")

    print("\nNote: BFS shortest path A->F was A->C->F (2 hops).")
    print(      "      DFS found:              ", " -> ".join(path),
                f"({len(path)-1} hops) — valid but not necessarily shortest.")
