"""
usps_denver_dataset.py
======================
Real-world test dataset: USPS letter-carrier delivery route
City:    Denver, Colorado — Capitol Hill neighborhood (ZIP 80203)
Source:  Street layout matches the actual Capitol Hill grid.
         Edge weights are approximate walking/driving distances in feet.

Network overview
----------------
The letter-carrier departs Capitol Hill Station Post Office (PO) and covers
a 4-block × 4-block delivery zone bounded by:

  E–W streets (south → north) : E 12th Ave, E Colfax Ave, E 14th Ave, E 15th Ave
  N–S streets (west → east)   : Logan St, Pennsylvania St, Pearl St, Clarkson St

One-way traffic (Denver's actual street directions, modeled as directed edges):
  E Colfax Ave    → EASTBOUND only   (COL_LOG → COL_PENN → COL_PEARL → COL_CLK)
  Logan St        → SOUTHBOUND only  (15_LOG  → 14_LOG   → COL_LOG   → 12_LOG)
  Pennsylvania St → NORTHBOUND only  (12_PENN → COL_PENN → 14_PENN   → 15_PENN)
  Pearl St        → SOUTHBOUND only  (15_PEARL→ 14_PEARL → COL_PEARL → 12_PEARL)
  Clarkson St     → NORTHBOUND only  (12_CLK  → COL_CLK  → 14_CLK   → 15_CLK)

Two-way streets (both directions explicitly as directed edges):
  E 12th Ave  300 ft / block
  E 14th Ave  310 ft / block
  E 15th Ave  310 ft / block

Grid map (north is up, one-way arrows show allowed travel direction):

              Logan      Penn       Pearl    Clarkson
  E 15th  [15_LOG]--[15_PENN]--[15_PEARL]--[15_CLK]
             ↓          ↑          ↓           ↑
  E 14th  [14_LOG]--[14_PENN]--[14_PEARL]--[14_CLK]
             ↓          ↑          ↓           ↑
  Colfax [COL_LOG]→[COL_PENN]→[COL_PEARL]→[COL_CLK]
             ↓          ↑          ↓           ↑
  E 12th  [12_LOG]--[12_PENN]--[12_PEARL]--[12_CLK]
                       |
                      [PO]   ← Capitol Hill Station Post Office
                               (~100 ft south of E 12th & Pennsylvania)

  ↑↓ = one-way on N–S streets    → = one-way eastbound (Colfax)
  -- = two-way (12th, 14th, 15th)

Real-world landmark context:
  PO        – Capitol Hill Station Post Office  (~1290 E 9th Ave / off Pennsylvania)
  COL_PENN  – Colfax & Pennsylvania             (bar/nightlife corridor)
  14_PENN   – E 14th & Pennsylvania             (near Molly Brown House, 1340 Penn St)
  15_LOG    – E 15th & Logan                    (near Colorado State Capitol grounds)
  COL_CLK   – Colfax & Clarkson                 (commercial strip, bodegas/restaurants)

Verified shortest delivery paths from PO (computed by Dijkstra):
  PO → 12_LOG    :   400 ft   PO → 12_PENN → 12_LOG
  PO → COL_PENN  :   450 ft   PO → 12_PENN → COL_PENN
  PO → 14_PENN   :   800 ft   PO → 12_PENN → COL_PENN → 14_PENN
  PO → 15_PENN   : 1,150 ft   PO → 12_PENN → COL_PENN → 14_PENN → 15_PENN
  PO → COL_CLK   : 1,050 ft   PO → 12_PENN → 12_PEARL → 12_CLK → COL_CLK
  PO → 14_CLK    : 1,400 ft   ... → COL_CLK → 14_CLK
  PO → 15_LOG    : 1,460 ft   ... → 15_PENN → 15_LOG
  PO → 15_CLK    : 1,750 ft   ... → 14_CLK  → 15_CLK
"""

import sys
import os
import io
import contextlib

sys.path.insert(0, os.path.dirname(__file__))

from graph_adj_list   import Graph as AdjListGraph
from graph_adj_matrix import Graph as AdjMatrixGraph
from graph_traversal  import dfs, bfs
from shortest_path    import dijkstra, shortest_path


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

# Vertex labels — each is a street intersection in Capitol Hill, Denver
VERTICES = [
    "PO",                                           # post office (source)
    "12_LOG",  "12_PENN",  "12_PEARL",  "12_CLK",  # E 12th Ave corridor
    "COL_LOG", "COL_PENN", "COL_PEARL", "COL_CLK", # E Colfax Ave corridor
    "14_LOG",  "14_PENN",  "14_PEARL",  "14_CLK",  # E 14th Ave corridor
    "15_LOG",  "15_PENN",  "15_PEARL",  "15_CLK",  # E 15th Ave corridor
]

# Directed edges: (src, dst, distance_in_feet)
EDGES = [
    # Post office exit / return  (~100 ft off E 12th & Pennsylvania)
    ("PO",        "12_PENN",   100),
    ("12_PENN",   "PO",        100),

    # E 12th Ave — two-way, 300 ft per block ---------------------------------
    ("12_LOG",    "12_PENN",   300),
    ("12_PENN",   "12_LOG",    300),
    ("12_PENN",   "12_PEARL",  300),
    ("12_PEARL",  "12_PENN",   300),
    ("12_PEARL",  "12_CLK",    300),
    ("12_CLK",    "12_PEARL",  300),

    # E Colfax Ave — ONE-WAY EAST, 330 ft per block --------------------------
    ("COL_LOG",   "COL_PENN",  330),
    ("COL_PENN",  "COL_PEARL", 330),
    ("COL_PEARL", "COL_CLK",   330),

    # E 14th Ave — two-way, 310 ft per block ---------------------------------
    ("14_LOG",    "14_PENN",   310),
    ("14_PENN",   "14_LOG",    310),
    ("14_PENN",   "14_PEARL",  310),
    ("14_PEARL",  "14_PENN",   310),
    ("14_PEARL",  "14_CLK",    310),
    ("14_CLK",    "14_PEARL",  310),

    # E 15th Ave — two-way, 310 ft per block ---------------------------------
    ("15_LOG",    "15_PENN",   310),
    ("15_PENN",   "15_LOG",    310),
    ("15_PENN",   "15_PEARL",  310),
    ("15_PEARL",  "15_PENN",   310),
    ("15_PEARL",  "15_CLK",    310),
    ("15_CLK",    "15_PEARL",  310),

    # Logan St — ONE-WAY SOUTH, 350 ft per block -----------------------------
    ("15_LOG",    "14_LOG",    350),
    ("14_LOG",    "COL_LOG",   350),
    ("COL_LOG",   "12_LOG",    350),

    # Pennsylvania St — ONE-WAY NORTH, 350 ft per block ----------------------
    ("12_PENN",   "COL_PENN",  350),
    ("COL_PENN",  "14_PENN",   350),
    ("14_PENN",   "15_PENN",   350),

    # Pearl St — ONE-WAY SOUTH, 350 ft per block -----------------------------
    ("15_PEARL",  "14_PEARL",  350),
    ("14_PEARL",  "COL_PEARL", 350),
    ("COL_PEARL", "12_PEARL",  350),

    # Clarkson St — ONE-WAY NORTH, 350 ft per block --------------------------
    ("12_CLK",    "COL_CLK",   350),
    ("COL_CLK",   "14_CLK",    350),
    ("14_CLK",    "15_CLK",    350),
]

# Pre-computed shortest delivery routes from PO.
# Each tuple: (destination, expected_feet, expected_path_list)
# All paths are unique (no ties) — safe to assert exact path.
KNOWN_ROUTES = [
    ("12_LOG",   400,  ["PO", "12_PENN", "12_LOG"]),
    ("COL_PENN", 450,  ["PO", "12_PENN", "COL_PENN"]),
    ("14_PENN",  800,  ["PO", "12_PENN", "COL_PENN", "14_PENN"]),
    ("15_PENN",  1150, ["PO", "12_PENN", "COL_PENN", "14_PENN", "15_PENN"]),
    ("COL_CLK",  1050, ["PO", "12_PENN", "12_PEARL", "12_CLK", "COL_CLK"]),
    ("14_CLK",   1400, ["PO", "12_PENN", "12_PEARL", "12_CLK", "COL_CLK", "14_CLK"]),
    ("15_LOG",   1460, ["PO", "12_PENN", "COL_PENN", "14_PENN", "15_PENN", "15_LOG"]),
    ("15_CLK",   1750, ["PO", "12_PENN", "12_PEARL", "12_CLK", "COL_CLK", "14_CLK", "15_CLK"]),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_graphs():
    """Return (AdjListGraph, AdjMatrixGraph) both built from the Denver dataset."""
    gl = AdjListGraph(directed=True)
    gm = AdjMatrixGraph(directed=True)
    for v in VERTICES:
        gl.add_vertex(v)
        gm.add_vertex(v)
    for src, dst, w in EDGES:
        gl.add_edge(src, dst, w)
        gm.add_edge(src, dst, w)
    return gl, gm


def _silent(fn, *args, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return fn(*args, **kwargs)


# ---------------------------------------------------------------------------
# Demo: shortest delivery paths (Dijkstra)
# ---------------------------------------------------------------------------

def run_delivery_demo(graph, label="Adjacency List"):
    """Print Dijkstra shortest-path table from PO to every intersection."""
    print(f"\n{'=' * 65}")
    print(f"DIJKSTRA DELIVERY TABLE — {label}")
    print(f"Source: Capitol Hill Station Post Office (PO)")
    print(f"{'=' * 65}")

    dist, pred = _silent(dijkstra, graph, "PO")

    print(f"  {'Destination':<14}  {'Distance (ft)':>14}  Route")
    print(f"  {'-'*14}  {'-'*14}  {'-'*35}")

    for v in VERTICES:
        if v == "PO":
            continue
        d = dist[v]
        if d == float("inf"):
            d_str, route_str = "unreachable", "—"
        else:
            d_str = f"{d:,}"
            path, _ = _silent(shortest_path, graph, "PO", v)
            route_str = " → ".join(path)
        print(f"  {v:<14}  {d_str:>14}  {route_str}")


# ---------------------------------------------------------------------------
# Demo: BFS / DFS coverage
# ---------------------------------------------------------------------------

def run_traversal_demo(graph, label="Adjacency List"):
    """BFS and DFS from PO — confirms all 17 intersections are reachable."""
    print(f"\n{'=' * 65}")
    print(f"TRAVERSAL COVERAGE — {label}")
    print(f"{'=' * 65}")

    bfs_order = _silent(bfs, graph, "PO")
    dfs_order = _silent(dfs, graph, "PO")

    print(f"  BFS from PO  ({len(bfs_order)}/{len(VERTICES)} intersections):")
    print(f"    " + " → ".join(bfs_order))

    print(f"\n  DFS from PO  ({len(dfs_order)}/{len(VERTICES)} intersections):")
    print(f"    " + " → ".join(dfs_order))

    unreachable = [v for v in VERTICES if v not in set(bfs_order)]
    if unreachable:
        print(f"\n  [!] NOT reachable from PO: {', '.join(unreachable)}")
    else:
        print(f"\n  All {len(VERTICES)} intersections reachable from PO.")

    bfs_levels = _bfs_levels(graph, "PO")
    print(f"\n  BFS delivery layers (fewest turns from PO):")
    for level, nodes in enumerate(bfs_levels):
        print(f"    Layer {level}: {', '.join(nodes)}")


def _bfs_levels(graph, start):
    """Return BFS layers as a list of lists (nodes at each hop distance)."""
    from collections import deque
    visited = {start}
    queue = deque([(start, 0)])
    layers = []
    while queue:
        node, depth = queue.popleft()
        if depth == len(layers):
            layers.append([])
        layers[depth].append(node)
        raw = graph.get_neighbors(node)
        neighbors = [nb for nb, _ in raw] if raw and isinstance(raw[0], tuple) else raw
        for nb in neighbors:
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, depth + 1))
    return layers


# ---------------------------------------------------------------------------
# Assertions: verify known shortest paths
# ---------------------------------------------------------------------------

def run_assertions(graph, label=""):
    """Assert all KNOWN_ROUTES match Dijkstra output. Returns True if all pass."""
    tag = f" [{label}]" if label else ""
    print(f"\n{'=' * 65}")
    print(f"ASSERTION CHECKS{tag}")
    print(f"{'=' * 65}")

    passed = failed = 0

    for dst, expected_ft, expected_path in KNOWN_ROUTES:
        actual_path, actual_ft = _silent(shortest_path, graph, "PO", dst)
        cost_ok = actual_ft == expected_ft
        path_ok = actual_path == expected_path
        ok = cost_ok and path_ok

        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1

        route_str = " → ".join(expected_path)
        print(f"  {status}  PO → {dst:<12}  {expected_ft:>6,} ft  {route_str}")

        if not cost_ok:
            print(f"         !! cost: expected {expected_ft}, got {actual_ft}")
        if not path_ok:
            print(f"         !! path expected: {expected_path}")
            print(f"                 got:      {actual_path}")

    print(f"\n  {passed}/{passed + failed} assertions passed{tag}")
    return failed == 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    gl, gm = build_graphs()

    print("=" * 65)
    print("Denver, CO — Capitol Hill USPS Delivery Route")
    print("=" * 65)
    print(f"  City     : Denver, Colorado (ZIP 80203)")
    print(f"  Area     : Capitol Hill — E 12th Ave to E 15th Ave,")
    print(f"             Logan St to Clarkson St")
    print(f"  Vertices : {len(VERTICES)}  (post office + 16 intersections)")
    print(f"  Edges    : {len(EDGES)}  (directed; one-way streets explicit)")
    print(f"  Weights  : street distance in feet")
    print(f"  Source   : PO (Capitol Hill Station Post Office)")

    # Delivery route tables
    run_delivery_demo(gl, "Adjacency List")
    run_delivery_demo(gm, "Adjacency Matrix")

    # BFS / DFS coverage
    run_traversal_demo(gl, "Adjacency List")

    # Known-answer assertions for both representations
    all_pass = True
    all_pass &= run_assertions(gl, "adj-list")
    all_pass &= run_assertions(gm, "adj-matrix")

    print("\n" + "=" * 65)
    if all_pass:
        print("All assertions passed for both graph representations.")
    else:
        print("Some assertions FAILED — see details above.")
    print("=" * 65)
