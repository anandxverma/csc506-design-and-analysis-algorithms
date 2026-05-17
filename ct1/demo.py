#!/usr/bin/python3
"""
demo.py — Auto-running demo for screen recording.

Launches the full GUI, then drives it through all five tabs automatically:
  0:00  Intro title card overlay
  0:10  Stack tab  — push 5 items, peek, pop 2
  0:55  Queue tab  — enqueue 5 items, peek, dequeue 2
  1:40  Linked List tab — append 3, prepend 2, search, delete
  2:30  Complexity tab — highlight every row in all three sections
  3:10  Performance tab — run live benchmark, wait for charts & report
  ~4:45 End overlay

Run it, then start your screen recorder, or start recording first.
Close the window at any time to stop.
"""

import sys
import os
import time
import tkinter as tk
from tkinter import ttk

# Make sure local modules resolve correctly
sys.path.insert(0, os.path.dirname(__file__))

import gui as _gui_module
from gui import (
    App, StackTab, QueueTab, LinkedListTab, ComplexityTab, PerfTab,
    BG, BG2, SURFACE, TEXT, SUBTEXT, BLUE, GREEN, YELLOW, ORANGE,
    RED, PURPLE, TEAL, MUTED,
)


# ── Timing helpers ──────────────────────────────────────────────────────────

FAST = False   # set True to compress waits (useful for testing the script)

def _ms(ms: int) -> int:
    """Scale delay: normal pace vs fast-test mode."""
    return max(60, ms // 8) if FAST else ms


# ── Overlay banner ──────────────────────────────────────────────────────────

class Overlay:
    """Translucent banner drawn on the root window for section titles."""

    def __init__(self, root: tk.Tk):
        self._root = root
        self._canvas = tk.Canvas(root, bg=BG2, highlightthickness=0, height=54)
        self._id = None

    def show(self, line1: str, line2: str = "", color=BLUE):
        self._canvas.place(relx=0, rely=0, relwidth=1)
        self._canvas.delete("all")
        self._canvas.create_rectangle(0, 0, 9000, 54, fill=BG2, outline="")
        self._canvas.create_text(
            20, 16, text=line1, anchor="w",
            fill=color, font=("Courier", 13, "bold")
        )
        if line2:
            self._canvas.create_text(
                20, 36, text=line2, anchor="w",
                fill=SUBTEXT, font=("Courier", 9)
            )
        self._root.update()

    def hide(self):
        self._canvas.place_forget()
        self._root.update()


# ── Tab helpers ─────────────────────────────────────────────────────────────

def _select_tab(nb: ttk.Notebook, index: int):
    nb.select(index)


def _set_entry(tab, value: str):
    tab._entry.delete(0, tk.END)
    tab._entry.insert(0, value)


def _flash_entry(tab, value: str, app: tk.Tk, pause_ms: int = 500):
    """Type a value character-by-character to make it visible on screen."""
    tab._entry.delete(0, tk.END)
    for ch in value:
        tab._entry.insert(tk.END, ch)
        app.update()
        app.after(_ms(55))
        time.sleep(0.001)
    app.after(_ms(pause_ms))
    app.update()


def _highlight_notebook_tab(nb: ttk.Notebook, index: int, app: tk.Tk):
    """Flash the notebook tab text to draw viewer attention."""
    nb.select(index)
    app.update()
    app.after(_ms(300))
    app.update()


# ── Section demos ───────────────────────────────────────────────────────────

def _demo_stack(app: App, nb: ttk.Notebook, overlay: Overlay):
    overlay.show(
        "  Stack  (LIFO — Last In, First Out)",
        "  Backed by Python list · Push & Pop are O(1) · Search is O(n)",
        BLUE,
    )
    app.after(_ms(1800))
    app.update()
    overlay.hide()

    tab: StackTab = nb.tabs()  # resolved below via winfo_children
    # Grab the StackTab instance from the notebook
    frames = [nb.nametowidget(t) for t in nb.tabs()]
    stack_tab: StackTab = frames[0]

    pushes = ["apple", "banana", "cherry", "date", "elderberry"]
    for val in pushes:
        _flash_entry(stack_tab, val, app, pause_ms=200)
        stack_tab._push()
        app.after(_ms(650))
        app.update()

    # Peek
    app.after(_ms(400))
    stack_tab._peek()
    app.after(_ms(900))
    app.update()

    # Pop twice
    for _ in range(2):
        stack_tab._pop()
        app.after(_ms(800))
        app.update()


def _demo_queue(app: App, nb: ttk.Notebook, overlay: Overlay):
    frames = [nb.nametowidget(t) for t in nb.tabs()]
    queue_tab: QueueTab = frames[1]

    overlay.show(
        "  Queue  (FIFO — First In, First Out)",
        "  Backed by collections.deque · Enqueue & Dequeue are O(1)",
        GREEN,
    )
    app.after(_ms(1800))
    app.update()
    overlay.hide()

    items = ["task-1", "task-2", "task-3", "task-4", "task-5"]
    for val in items:
        _flash_entry(queue_tab, val, app, pause_ms=200)
        queue_tab._enqueue()
        app.after(_ms(650))
        app.update()

    # Peek
    app.after(_ms(400))
    queue_tab._peek()
    app.after(_ms(900))
    app.update()

    # Dequeue twice
    for _ in range(2):
        queue_tab._dequeue()
        app.after(_ms(800))
        app.update()


def _demo_linked_list(app: App, nb: ttk.Notebook, overlay: Overlay):
    frames = [nb.nametowidget(t) for t in nb.tabs()]
    ll_tab: LinkedListTab = frames[2]

    overlay.show(
        "  Linked List  (Singly linked, pointer-chased)",
        "  Prepend O(1) · Append O(n) · Delete/Search O(n) worst case",
        ORANGE,
    )
    app.after(_ms(1800))
    app.update()
    overlay.hide()

    # Append 3
    for val in ["node-A", "node-B", "node-C"]:
        _flash_entry(ll_tab, val, app, pause_ms=200)
        ll_tab._append()
        app.after(_ms(700))
        app.update()

    # Prepend 2
    for val in ["node-Z", "node-Y"]:
        _flash_entry(ll_tab, val, app, pause_ms=200)
        ll_tab._prepend()
        app.after(_ms(700))
        app.update()

    # Search — found
    _flash_entry(ll_tab, "node-B", app, pause_ms=300)
    ll_tab._search()
    app.after(_ms(900))
    app.update()

    # Search — not found
    _flash_entry(ll_tab, "node-X", app, pause_ms=300)
    ll_tab._search()
    app.after(_ms(900))
    app.update()

    # Delete one node
    _flash_entry(ll_tab, "node-B", app, pause_ms=300)
    ll_tab._delete()
    app.after(_ms(900))
    app.update()


def _demo_complexity(app: App, nb: ttk.Notebook, overlay: Overlay):
    frames = [nb.nametowidget(t) for t in nb.tabs()]
    complexity_tab: ComplexityTab = frames[3]

    overlay.show(
        "  Complexity Reference  — Big-O for every operation",
        "  Click any row to see an explanation at the bottom",
        PURPLE,
    )
    app.after(_ms(1800))
    app.update()
    overlay.hide()

    # Walk through every operation row by calling _show_detail directly
    from gui import _COMPLEXITY_DATA
    for ds_name, ops in _COMPLEXITY_DATA.items():
        for op_name, (best, worst, explanation) in ops.items():
            complexity_tab._show_detail(op_name, best, worst, explanation)
            app.update()
            app.after(_ms(900))

    app.after(_ms(600))
    app.update()


def _demo_performance(app: App, nb: ttk.Notebook, overlay: Overlay):
    frames = [nb.nametowidget(t) for t in nb.tabs()]
    perf_tab: PerfTab = frames[4]

    overlay.show(
        "  Performance Benchmark — live measurement across 8 input sizes",
        "  Measures Stack, Queue, Linked List · Fits O(1) & O(n) curves",
        YELLOW,
    )
    app.after(_ms(2000))
    app.update()
    overlay.hide()

    # Trigger the benchmark — it runs in a background thread
    perf_tab._start_benchmark()

    # Poll until benchmark finishes (max 120 s)
    deadline = time.time() + 120
    while perf_tab._running and time.time() < deadline:
        app.update()
        time.sleep(0.1)

    # Let the charts settle
    app.after(_ms(1200))
    app.update()

    # Switch to Report sub-tab
    perf_tab._inner_nb.select(1)
    app.after(_ms(2500))
    app.update()

    # Switch back to Charts sub-tab
    perf_tab._inner_nb.select(0)
    app.after(_ms(1500))
    app.update()


# ── Outro overlay ───────────────────────────────────────────────────────────

def _outro(app: App, overlay: Overlay):
    overlay.show(
        "  Demo complete — Data Structures Interactive Tool",
        "  CSC 506 · Colorado State University · github.com/anandxverma",
        TEAL,
    )
    app.after(_ms(4000))
    app.update()
    overlay.hide()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    app = App()

    # Locate the top-level notebook (second child after the header label)
    nb: ttk.Notebook = None
    for child in app.winfo_children():
        if isinstance(child, ttk.Notebook):
            nb = child
            break

    if nb is None:
        raise RuntimeError("Could not find the main Notebook widget.")

    overlay = Overlay(app)

    # Intro
    overlay.show(
        "  Data Structures — Interactive Demo",
        "  Stack · Queue · Linked List · Complexity · Performance",
        BLUE,
    )
    app.after(_ms(2500))
    app.update()
    overlay.hide()
    app.after(_ms(400))
    app.update()

    # ── Tab 0: Stack ──
    _highlight_notebook_tab(nb, 0, app)
    _demo_stack(app, nb, overlay)
    app.after(_ms(700))
    app.update()

    # ── Tab 1: Queue ──
    _highlight_notebook_tab(nb, 1, app)
    _demo_queue(app, nb, overlay)
    app.after(_ms(700))
    app.update()

    # ── Tab 2: Linked List ──
    _highlight_notebook_tab(nb, 2, app)
    _demo_linked_list(app, nb, overlay)
    app.after(_ms(700))
    app.update()

    # ── Tab 3: Complexity ──
    _highlight_notebook_tab(nb, 3, app)
    _demo_complexity(app, nb, overlay)
    app.after(_ms(700))
    app.update()

    # ── Tab 4: Performance ──
    _highlight_notebook_tab(nb, 4, app)
    _demo_performance(app, nb, overlay)
    app.after(_ms(700))
    app.update()

    # Outro
    _outro(app, overlay)

    # Hand control back to user
    app.mainloop()


if __name__ == "__main__":
    # Pass --fast to speed through (for testing)
    if "--fast" in sys.argv:
        FAST = True
    main()
