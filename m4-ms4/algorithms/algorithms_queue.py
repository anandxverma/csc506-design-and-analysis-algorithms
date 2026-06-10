"""
Queue-based algorithms — three classic problems where FIFO ordering is essential.

Imports the Queue class from queue.py in the same package.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from queue import Queue


# ---------------------------------------------------------------------------
# Algorithm 1: Breadth-First Search (BFS) on an unweighted graph
# ---------------------------------------------------------------------------

def bfs(graph: dict, start: str) -> list[str]:
    """
    Visit every reachable vertex in level order from `start`.

    The queue guarantees that all vertices at distance d are processed before
    any vertex at distance d+1, producing the shortest-hop traversal order.
    Time: O(V + E)  Space: O(V)
    """
    visited = {start}
    order = []
    q = Queue()
    q.enqueue(start)

    while not q.is_empty():
        vertex = q.dequeue()
        order.append(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                q.enqueue(neighbor)

    return order


def bfs_shortest_path(graph: dict, start: str, goal: str) -> list[str] | None:
    """
    Return the shortest path (fewest hops) from start to goal using BFS.
    Returns None if no path exists.
    """
    if start == goal:
        return [start]

    visited = {start}
    # Queue stores (current_vertex, path_so_far)
    q = Queue()
    q.enqueue((start, [start]))

    while not q.is_empty():
        vertex, path = q.dequeue()
        for neighbor in graph.get(vertex, []):
            if neighbor == goal:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                q.enqueue((neighbor, path + [neighbor]))

    return None


# ---------------------------------------------------------------------------
# Algorithm 2: Level-Order Binary Tree Traversal
# ---------------------------------------------------------------------------

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order(root: TreeNode | None) -> list[list]:
    """
    Return each level of the tree as its own list.

    A queue naturally maps to tree levels: dequeue a node, process it, then
    enqueue its children. Because children are enqueued after all siblings,
    nodes within the same level are always contiguous in the queue.
    Time: O(N)  Space: O(W) where W is the maximum width of the tree.
    """
    if root is None:
        return []

    result = []
    q = Queue()
    q.enqueue(root)

    while not q.is_empty():
        level_size = q.size()   # snapshot: how many nodes are on this level
        level = []
        for _ in range(level_size):
            node = q.dequeue()
            level.append(node.val)
            if node.left:
                q.enqueue(node.left)
            if node.right:
                q.enqueue(node.right)
        result.append(level)

    return result


# ---------------------------------------------------------------------------
# Algorithm 3: Round-Robin CPU Scheduler
# ---------------------------------------------------------------------------

def round_robin(processes: list[dict], quantum: int) -> dict:
    """
    Simulate a Round-Robin CPU scheduler with a fixed time quantum.

    Each process is a dict with keys 'name' and 'burst' (remaining CPU time).
    The ready queue cycles through processes in arrival order; any process
    that still has remaining burst time after its quantum is re-enqueued.

    Returns a dict with:
      - 'timeline': list of (process_name, start, end) slices
      - 'turnaround': dict mapping process name -> turnaround time
      - 'waiting':    dict mapping process name -> waiting time
    """
    q = Queue()
    for p in processes:
        q.enqueue({'name': p['name'], 'burst': p['burst']})

    arrival = {p['name']: 0 for p in processes}  # all arrive at t=0
    finish = {}
    timeline = []
    clock = 0

    while not q.is_empty():
        proc = q.dequeue()
        run = min(proc['burst'], quantum)
        timeline.append((proc['name'], clock, clock + run))
        clock += run
        proc['burst'] -= run
        if proc['burst'] > 0:
            q.enqueue(proc)
        else:
            finish[proc['name']] = clock

    turnaround = {name: finish[name] - arrival[name] for name in finish}
    waiting    = {name: turnaround[name] - sum(
                      p['burst'] for p in processes if p['name'] == name
                  ) for name in finish}

    return {'timeline': timeline, 'turnaround': turnaround, 'waiting': waiting}


# ---------------------------------------------------------------------------
# Demo / main
# ---------------------------------------------------------------------------

def separator(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


if __name__ == "__main__":

    # ------------------------------------------------------------------
    # Demo 1: BFS
    # ------------------------------------------------------------------
    separator("Algorithm 1: Breadth-First Search (BFS)")
    print("""
Description:
  BFS explores a graph layer by layer, starting from a source vertex.
  It uses a FIFO queue so that vertices discovered earlier are also
  visited earlier, guaranteeing the shortest-hop path to every reachable
  vertex in an unweighted graph.
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

    print("Graph adjacency list:")
    for v, nbrs in graph.items():
        print(f"  {v} -> {nbrs}")

    traversal = bfs(graph, 'A')
    print(f"\nBFS traversal from 'A': {traversal}")

    path = bfs_shortest_path(graph, 'A', 'F')
    print(f"Shortest path from 'A' to 'F': {' -> '.join(path)}")

    path2 = bfs_shortest_path(graph, 'D', 'C')
    print(f"Shortest path from 'D' to 'C': {' -> '.join(path2)}")

    # ------------------------------------------------------------------
    # Demo 2: Level-Order Tree Traversal
    # ------------------------------------------------------------------
    separator("Algorithm 2: Level-Order Binary Tree Traversal")
    print("""
Description:
  Level-order traversal visits every node in a binary tree row by row,
  top to bottom and left to right.  A queue drives the process: enqueue
  the root, then repeatedly dequeue a node, record its value, and enqueue
  its children.  Snapshotting the queue size before processing each batch
  isolates individual levels without needing depth tracking.
  Time complexity: O(N)
""")

    #        1
    #       / \\
    #      2   3
    #     / \\ / \\
    #    4  5 6  7
    root = TreeNode(1,
             TreeNode(2, TreeNode(4), TreeNode(5)),
             TreeNode(3, TreeNode(6), TreeNode(7)))

    print("Tree structure:")
    print("        1")
    print("       / \\")
    print("      2   3")
    print("     / \\ / \\")
    print("    4  5 6  7")

    levels = level_order(root)
    print(f"\nLevel-order levels: {levels}")
    for i, lvl in enumerate(levels):
        print(f"  Level {i}: {lvl}")

    # ------------------------------------------------------------------
    # Demo 3: Round-Robin Scheduler
    # ------------------------------------------------------------------
    separator("Algorithm 3: Round-Robin CPU Scheduling")
    print("""
Description:
  Round-Robin is a preemptive CPU scheduling algorithm in which each
  ready process receives a fixed slice of CPU time called a quantum.
  If a process does not finish within its quantum it is re-enqueued at
  the tail, giving every process a fair, equal turn.  The FIFO queue
  enforces arrival order and prevents starvation.
  Time complexity: O(N * ceil(burst_max / quantum))
""")

    processes = [
        {'name': 'P1', 'burst': 10},
        {'name': 'P2', 'burst': 4},
        {'name': 'P3', 'burst': 6},
        {'name': 'P4', 'burst': 3},
    ]
    quantum = 4

    proc_summary = [f"{p['name']}(burst={p['burst']})" for p in processes]
    print(f"Processes: {proc_summary}")
    print(f"Time quantum: {quantum}\n")

    result = round_robin(processes, quantum)

    print("Execution timeline:")
    for name, start, end in result['timeline']:
        bar = '#' * (end - start)
        print(f"  t={start:>2}-{end:<2}  {name}  [{bar}]")

    print("\nTurnaround times (finish - arrival):")
    for name, tt in result['turnaround'].items():
        print(f"  {name}: {tt}")

    print("\nWaiting times (turnaround - burst):")
    for name, wt in result['waiting'].items():
        print(f"  {name}: {wt}")

    avg_tat = sum(result['turnaround'].values()) / len(result['turnaround'])
    avg_wt  = sum(result['waiting'].values())    / len(result['waiting'])
    print(f"\nAverage turnaround: {avg_tat:.2f}")
    print(f"Average waiting:    {avg_wt:.2f}")
