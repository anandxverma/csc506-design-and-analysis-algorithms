"""
generate_report.py
==================
Runs the benchmark from performance_analysis.py and produces a PDF report
containing:
  - Cover / summary section
  - Raw timing table (all scenarios)
  - Four charts:
      1. Hit-search latency vs. n  (random insertion — BST vs. List)
      2. Miss-search latency vs. n (random insertion — BST vs. List)
      3. Hit-search latency vs. n  (sorted insertion — BST vs. List)
      4. Speed-ratio (list / BST)  for hit & miss across both insertion orders
  - Complexity-growth analysis tables
  - Theoretical complexity summary

Usage
-----
    python generate_report.py
    # → prompts for output path, defaults to ./report.pdf
"""

import os
import sys
import math
import random
import io

import matplotlib
matplotlib.use("Agg")          # non-interactive backend — no display needed
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, PageBreak, KeepTogether,
)

# ---------------------------------------------------------------------------
# Import benchmark code from sibling module
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(__file__))
sys.setrecursionlimit(20_000)

from performance_analysis import run_benchmark, SIZES, REPEATS

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
BST_RANDOM_HIT   = "#2196F3"   # blue
BST_RANDOM_MISS  = "#64B5F6"   # light blue
BST_SORTED_HIT   = "#F44336"   # red
BST_SORTED_MISS  = "#EF9A9A"   # light red
LIST_HIT         = "#4CAF50"   # green
LIST_MISS        = "#A5D6A7"   # light green
RATIO_RANDOM     = "#9C27B0"   # purple
RATIO_SORTED     = "#FF9800"   # orange

HEADER_BG        = colors.HexColor("#1565C0")
ALT_ROW          = colors.HexColor("#E3F2FD")
BORDER           = colors.HexColor("#90CAF9")


# ===========================================================================
# 1.  Run benchmarks
# ===========================================================================

def collect_results():
    random.seed(42)
    print("Running benchmarks …", flush=True)
    results = []
    for order in ("random", "sorted"):
        for size in SIZES:
            print(f"  {order:8s}  n={size:>6,} … ", end="", flush=True)
            r = run_benchmark(size, order)
            results.append(r)
            print(f"done  (tree-hit={r['tree_hit_us']:.4f} µs, "
                  f"list-hit={r['list_hit_us']:.4f} µs)")
    print()
    return results


# ===========================================================================
# 2.  Chart builders
# ===========================================================================

def _fig_to_image(fig, width_in=6.5):
    fig_w, fig_h = fig.get_size_inches()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    height_in = width_in * (fig_h / fig_w)
    img = Image(buf, width=width_in * inch, height=height_in * inch)
    img.hAlign = "CENTER"
    return img


def chart_hit_latency_random(random_results):
    sizes = [r["size"] for r in random_results]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(sizes, [r["tree_hit_us"] for r in random_results],
            "o-", color=BST_RANDOM_HIT, lw=2, label="BST (random)")
    ax.plot(sizes, [r["list_hit_us"] for r in random_results],
            "s-", color=LIST_HIT, lw=2, label="List")
    ax.set_title("Hit-Search Latency — Random Insertion", fontsize=13, fontweight="bold")
    ax.set_xlabel("Dataset size (n)")
    ax.set_ylabel("Avg µs per contains_key()")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    return _fig_to_image(fig)


def chart_miss_latency_random(random_results):
    sizes = [r["size"] for r in random_results]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(sizes, [r["tree_miss_us"] for r in random_results],
            "o-", color=BST_RANDOM_MISS, lw=2, label="BST (random)")
    ax.plot(sizes, [r["list_miss_us"] for r in random_results],
            "s-", color=LIST_MISS, lw=2, label="List")
    ax.set_title("Miss-Search Latency — Random Insertion", fontsize=13, fontweight="bold")
    ax.set_xlabel("Dataset size (n)")
    ax.set_ylabel("Avg µs per contains_key()")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    return _fig_to_image(fig)


def chart_hit_latency_sorted(sorted_results):
    sizes = [r["size"] for r in sorted_results]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(sizes, [r["tree_hit_us"] for r in sorted_results],
            "o-", color=BST_SORTED_HIT, lw=2, label="BST (sorted — degenerate)")
    ax.plot(sizes, [r["list_hit_us"] for r in sorted_results],
            "s-", color=LIST_HIT, lw=2, label="List")
    ax.set_title("Hit-Search Latency — Sorted Insertion (Worst Case)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Dataset size (n)")
    ax.set_ylabel("Avg µs per contains_key()")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    return _fig_to_image(fig)


def chart_speed_ratios(random_results, sorted_results):
    sizes = [r["size"] for r in random_results]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(sizes, [r["hit_ratio"]  for r in random_results],
            "o-", color=RATIO_RANDOM, lw=2, label="random — hit  (list / BST)")
    ax.plot(sizes, [r["miss_ratio"] for r in random_results],
            "o--", color=RATIO_RANDOM, lw=1.5, alpha=0.7, label="random — miss (list / BST)")
    ax.plot(sizes, [r["hit_ratio"]  for r in sorted_results],
            "s-", color=RATIO_SORTED, lw=2, label="sorted  — hit  (list / BST)")
    ax.axhline(1.0, color="gray", linestyle=":", lw=1.5, label="ratio = 1 (equal)")
    ax.set_title("Speed Ratio: List Time ÷ BST Time (>1 = BST faster)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Dataset size (n)")
    ax.set_ylabel("Ratio (list µs / BST µs)")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.legend(fontsize=8)
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    return _fig_to_image(fig)


def chart_log_scale_comparison(random_results, sorted_results):
    sizes = [r["size"] for r in random_results]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(sizes, [r["tree_hit_us"] for r in random_results],
            "o-", color=BST_RANDOM_HIT, lw=2, label="BST random (avg O(log n))")
    ax.plot(sizes, [r["tree_hit_us"] for r in sorted_results],
            "o-", color=BST_SORTED_HIT, lw=2, label="BST sorted (worst O(n))")
    ax.plot(sizes, [r["list_hit_us"] for r in random_results],
            "s-", color=LIST_HIT, lw=2, label="List O(n)")
    ax.set_title("Hit Latency — All Structures (log-scale y-axis)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Dataset size (n)")
    ax.set_ylabel("Avg µs per contains_key()  [log scale]")
    ax.set_yscale("log")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.legend()
    ax.grid(True, which="both", linestyle="--", alpha=0.5)
    fig.tight_layout()
    return _fig_to_image(fig)


# ===========================================================================
# 3.  ReportLab helpers
# ===========================================================================

def _styles():
    base = getSampleStyleSheet()
    title = ParagraphStyle(
        "ReportTitle",
        parent=base["Title"],
        fontSize=22,
        spaceAfter=8,
        textColor=colors.HexColor("#0D47A1"),
        alignment=TA_CENTER,
    )
    subtitle = ParagraphStyle(
        "Subtitle",
        parent=base["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#424242"),
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    h1 = ParagraphStyle(
        "H1", parent=base["Heading1"],
        fontSize=14, spaceAfter=6, spaceBefore=14,
        textColor=colors.HexColor("#1565C0"),
    )
    h2 = ParagraphStyle(
        "H2", parent=base["Heading2"],
        fontSize=11, spaceAfter=4, spaceBefore=10,
        textColor=colors.HexColor("#1976D2"),
    )
    body = ParagraphStyle(
        "Body", parent=base["Normal"],
        fontSize=9.5, leading=14, alignment=TA_JUSTIFY,
    )
    mono = ParagraphStyle(
        "Mono", parent=base["Code"],
        fontSize=8, leading=11,
    )
    return title, subtitle, h1, h2, body, mono


def _raw_timing_table(results):
    hdr = ["n", "Order", "BST-hit (µs)", "List-hit (µs)",
           "BST-miss (µs)", "List-miss (µs)", "Hit ratio", "Miss ratio"]
    rows = [hdr]
    for r in results:
        rows.append([
            f"{r['size']:,}",
            r["order"],
            f"{r['tree_hit_us']:.4f}",
            f"{r['list_hit_us']:.4f}",
            f"{r['tree_miss_us']:.4f}",
            f"{r['list_miss_us']:.4f}",
            f"{r['hit_ratio']:.2f}x",
            f"{r['miss_ratio']:.2f}x",
        ])

    col_widths = [0.65*inch, 0.65*inch, 1.0*inch, 1.0*inch,
                  1.05*inch, 1.05*inch, 0.8*inch, 0.8*inch]
    tbl = Table(rows, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND",   (0, 0), (-1, 0),  HEADER_BG),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0),  8),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",     (0, 1), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ALT_ROW]),
        ("GRID",         (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING",   (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 3),
    ]
    # separator after random block (rows 1–5)
    style_cmds.append(("LINEBELOW", (0, 5), (-1, 5), 1.5, colors.HexColor("#1565C0")))
    tbl.setStyle(TableStyle(style_cmds))
    return tbl


def _growth_table(label, pairs):
    hdr = ["n₁", "n₂", "BST growth", "List growth", "Expected BST"]
    rows = [hdr] + pairs
    col_widths = [0.7*inch, 0.7*inch, 1.1*inch, 1.1*inch, 1.2*inch]
    tbl = Table(rows, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  HEADER_BG),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 8),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ALT_ROW]),
        ("GRID",         (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING",   (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 3),
    ]))
    return tbl


def _complexity_table():
    hdr = ["Structure", "Insert", "Search (avg)", "Search (worst)"]
    rows = [
        hdr,
        ["BST Map — random insertion", "O(log n)", "O(log n)", "O(n)"],
        ["BST Map — sorted insertion", "O(n)",     "O(n)",     "O(n)"],
        ["List Map",                   "O(n)",      "O(n)",     "O(n)"],
    ]
    col_widths = [2.4*inch, 1.0*inch, 1.2*inch, 1.3*inch]
    tbl = Table(rows, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  HEADER_BG),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ALT_ROW]),
        ("GRID",         (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))
    return tbl


# ===========================================================================
# 4.  PDF builder
# ===========================================================================

def build_pdf(results, out_path):
    title_s, subtitle_s, h1_s, h2_s, body_s, mono_s = _styles()

    random_results = [r for r in results if r["order"] == "random"]
    sorted_results = [r for r in results if r["order"] == "sorted"]

    doc = SimpleDocTemplate(
        out_path,
        pagesize=LETTER,
        leftMargin=0.85*inch, rightMargin=0.85*inch,
        topMargin=0.9*inch,   bottomMargin=0.9*inch,
        title="Performance Analysis: Tree-Based Map vs. List-Based Map",
        author="CSC 506 — Design and Analysis of Algorithms",
    )

    story = []

    # ------------------------------------------------------------------
    # Cover
    # ------------------------------------------------------------------
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Performance Analysis Report", title_s))
    story.append(Paragraph("Tree-Based Map vs. List-Based Map — Search Operations", subtitle_s))
    story.append(Paragraph("CSC 506 · Design and Analysis of Algorithms", subtitle_s))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1565C0"),
                             spaceAfter=12))

    story.append(Paragraph(
        "This report compares the search performance of a Binary Search Tree (BST)-backed "
        "Map against a naïve List-backed Map across five dataset sizes "
        "(n = 100 – 10,000), two insertion orders (random and sorted), and two query "
        "types (hit — key present; miss — key absent). "
        "Each data point is the average of 500 × 50 = 25,000 individual <i>contains_key()</i> "
        "calls, reported in microseconds.",
        body_s,
    ))
    story.append(Spacer(1, 0.15*inch))

    # ------------------------------------------------------------------
    # Section 1 — Raw results table
    # ------------------------------------------------------------------
    story.append(Paragraph("1. Raw Benchmark Results", h1_s))
    story.append(Paragraph(
        "All timings are in µs per <i>contains_key()</i> call. "
        "The upper block uses random-shuffled insertion; the lower block uses sorted "
        "(worst-case) insertion. "
        "<b>Hit-ratio</b> and <b>miss-ratio</b> are List time ÷ BST time — values "
        "greater than 1 indicate the BST is faster.",
        body_s,
    ))
    story.append(Spacer(1, 0.1*inch))
    story.append(_raw_timing_table(results))

    story.append(PageBreak())

    # ------------------------------------------------------------------
    # Section 2 — Charts
    # ------------------------------------------------------------------
    story.append(Paragraph("2. Graphical Analysis", h1_s))

    story.append(Paragraph("2a. Hit-Search Latency (Random Insertion)", h2_s))
    story.append(Paragraph(
        "With randomly shuffled keys the BST remains roughly balanced (height ≈ log₂ n), "
        "producing latency that grows logarithmically while the List grows linearly.",
        body_s,
    ))
    story.append(chart_hit_latency_random(random_results))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("2b. Miss-Search Latency (Random Insertion)", h2_s))
    story.append(Paragraph(
        "A cache miss requires traversing to a leaf (BST) or scanning the entire list. "
        "The BST advantage is most pronounced here because every miss walks to the "
        "deepest level of the tree — still O(log n) — while the list always does O(n) work.",
        body_s,
    ))
    story.append(chart_miss_latency_random(random_results))

    story.append(PageBreak())

    story.append(Paragraph("2c. Hit-Search Latency — Sorted Insertion (Worst Case)", h2_s))
    story.append(Paragraph(
        "When keys are inserted in ascending order the BST degenerates into a "
        "right-skewed linked list (height = n − 1). Search then requires O(n) "
        "comparisons — matching, and sometimes exceeding, the List.",
        body_s,
    ))
    story.append(chart_hit_latency_sorted(sorted_results))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("2d. Speed-Ratio Across All Scenarios", h2_s))
    story.append(Paragraph(
        "The ratio List µs ÷ BST µs — values above 1 mean the BST is faster. "
        "Random-insertion ratios climb with n (the BST advantage grows). "
        "Sorted-insertion ratios hover near 1, confirming the degenerate case "
        "erases the BST advantage.",
        body_s,
    ))
    story.append(chart_speed_ratios(random_results, sorted_results))

    story.append(PageBreak())

    story.append(Paragraph("2e. Log-Scale Comparison — All Structures", h2_s))
    story.append(Paragraph(
        "Logarithmic y-axis makes the different growth curves immediately visible. "
        "The random-BST curve is nearly flat; the sorted-BST and List curves rise "
        "in parallel, confirming identical O(n) behaviour.",
        body_s,
    ))
    story.append(chart_log_scale_comparison(random_results, sorted_results))

    story.append(PageBreak())

    # ------------------------------------------------------------------
    # Section 3 — Complexity growth analysis
    # ------------------------------------------------------------------
    story.append(Paragraph("3. Complexity Growth Analysis", h1_s))

    story.append(Paragraph("3a. Random-Insertion BST — Expected O(log n) vs. O(n) for List", h2_s))
    random_pairs = []
    for i in range(1, len(random_results)):
        r1, r2 = random_results[i - 1], random_results[i]
        tree_g = r2["tree_hit_us"] / r1["tree_hit_us"]
        list_g = r2["list_hit_us"] / r1["list_hit_us"]
        log_r  = math.log2(r2["size"]) / math.log2(r1["size"])
        random_pairs.append([
            f"{r1['size']:,}",
            f"{r2['size']:,}",
            f"{tree_g:.2f}×",
            f"{list_g:.2f}×",
            f"{log_r:.2f}×  (log₂ ratio)",
        ])
    story.append(_growth_table("Random BST growth", random_pairs))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "The BST growth factor consistently stays below the List growth factor and "
        "tracks the log₂(n₂) / log₂(n₁) ratio, which is the expected multiplier "
        "for O(log n) algorithms.",
        body_s,
    ))

    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("3b. Sorted-Insertion BST — Degenerate O(n) vs. List O(n)", h2_s))
    sorted_pairs = []
    for i in range(1, len(sorted_results)):
        r1, r2 = sorted_results[i - 1], sorted_results[i]
        tree_g = r2["tree_hit_us"] / r1["tree_hit_us"]
        list_g = r2["list_hit_us"] / r1["list_hit_us"]
        size_r  = r2["size"] / r1["size"]
        sorted_pairs.append([
            f"{r1['size']:,}",
            f"{r2['size']:,}",
            f"{tree_g:.2f}×",
            f"{list_g:.2f}×",
            f"~{size_r:.0f}×  (n₂/n₁ expected)",
        ])
    story.append(_growth_table("Sorted BST growth", sorted_pairs))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "Both growth factors track n₂ / n₁, confirming that sorted insertion "
        "reduces the BST to an O(n) structure indistinguishable from a List.",
        body_s,
    ))

    story.append(PageBreak())

    # ------------------------------------------------------------------
    # Section 4 — Theoretical summary + conclusions
    # ------------------------------------------------------------------
    story.append(Paragraph("4. Theoretical Complexity Summary", h1_s))
    story.append(_complexity_table())
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("5. Conclusions", h1_s))
    story.append(Paragraph(
        "<b>5.1 Random insertion (average case).</b>  "
        "The BST-backed Map consistently outperforms the List at every dataset size tested. "
        "The speed advantage grows with n — at n = 10,000 the BST resolves a hit search "
        f"in roughly {random_results[-1]['hit_ratio']:.1f}× less time than the List. "
        "This matches the theoretical O(log n) vs. O(n) contrast.",
        body_s,
    ))
    story.append(Spacer(1, 0.08*inch))
    story.append(Paragraph(
        "<b>5.2 Sorted insertion (worst case).</b>  "
        "When keys arrive in ascending order the BST degenerates into a right-skewed "
        "chain of height n − 1. Every search must traverse the full chain in the worst "
        "case, collapsing performance to O(n) — on par with (or occasionally slower than) "
        "the List due to pointer-chasing overhead.",
        body_s,
    ))
    story.append(Spacer(1, 0.08*inch))
    story.append(Paragraph(
        "<b>5.3 Practical recommendation.</b>  "
        "A plain BST should only be preferred over a List when the insertion order is "
        "uncontrolled (i.e. effectively random). If sorted or partially sorted input is "
        "expected, a self-balancing tree (AVL, Red-Black) or a hash map should be used "
        "to guarantee O(log n) or O(1) search respectively.",
        body_s,
    ))
    story.append(Spacer(1, 0.08*inch))
    story.append(Paragraph(
        "<b>5.4 Miss searches.</b>  "
        "A key-absent (miss) lookup forces the BST to reach a null child — the deepest "
        "path in the tree. Despite this, the BST miss time still scales as O(log n) "
        "for random insertion, while the List must scan all n entries, making the "
        "BST advantage even more pronounced for miss queries at large n.",
        body_s,
    ))

    story.append(Spacer(1, 0.3*inch))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#90CAF9")))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph(
        f"Benchmark parameters: repeats = {REPEATS}, sample size = 50 keys per scenario, "
        "random seed = 42.",
        ParagraphStyle("footer", parent=getSampleStyleSheet()["Normal"],
                       fontSize=8, textColor=colors.gray, alignment=TA_CENTER),
    ))

    doc.build(story)


# ===========================================================================
# 5.  Entry point
# ===========================================================================

def ask_output_path():
    default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.pdf")
    prompt  = f"Enter output PDF path [{default}]: "
    try:
        user = input(prompt).strip()
    except EOFError:
        user = ""
    path = user if user else default

    # Expand ~ and resolve relative paths
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    # Ensure the directory exists
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist. Creating it …")
        os.makedirs(directory, exist_ok=True)

    # Ensure .pdf extension
    if not path.lower().endswith(".pdf"):
        path += ".pdf"

    return path


if __name__ == "__main__":
    out_path = ask_output_path()
    results  = collect_results()

    print(f"Building PDF report → {out_path}")
    build_pdf(results, out_path)
    print(f"Done. Report saved to: {out_path}")
