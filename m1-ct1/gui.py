#!/usr/bin/env python3
import sys
import os
import threading
import importlib.util as _ilu
_q_spec = _ilu.spec_from_file_location(
    "_stdlib_queue",
    __import__("sysconfig").get_path("stdlib") + "/queue.py")
_stdlib_queue = _ilu.module_from_spec(_q_spec)
_q_spec.loader.exec_module(_stdlib_queue)
del _ilu, _q_spec
import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sys.path.insert(0, os.path.dirname(__file__))
from stack import Stack
from queue import Queue
from linked_list import LinkedList
import benchmark

# ── Palette (Tokyo Night) ─────────────────────────────────────────────────────
BG      = "#1e1e2e"
BG2     = "#181825"
SURFACE = "#313244"
MUTED   = "#45475a"
TEXT    = "#cdd6f4"
SUBTEXT = "#a6adc8"
BLUE    = "#7aa2f7"
GREEN   = "#a6e3a1"
YELLOW  = "#f9e2af"
ORANGE  = "#fab387"
RED     = "#f38ba8"
PURPLE  = "#cba6f7"
TEAL    = "#94e2d5"


# ── Application root ──────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Structures — Interactive Demo")
        self.geometry("880x680")
        self.minsize(700, 560)
        self.configure(bg=BG)
        self._apply_styles()
        self._build()

    def _apply_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TNotebook", background=BG, borderwidth=0, tabmargins=[0, 0, 0, 0])
        s.configure("TNotebook.Tab",
                    background=SURFACE, foreground=SUBTEXT,
                    padding=[18, 7], font=("Courier", 11, "bold"))
        s.map("TNotebook.Tab",
              background=[("selected", BG2)],
              foreground=[("selected", TEXT)])
        s.configure("TFrame", background=BG)

    def _build(self):
        tk.Label(
            self, text="Data Structures — Interactive Demo",
            bg=BG, fg=BLUE, font=("Courier", 15, "bold")
        ).pack(pady=(14, 8))

        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 14))

        for cls, label in [
            (StackTab,       "  Stack  "),
            (QueueTab,       "  Queue  "),
            (LinkedListTab,  "  Linked List  "),
            (ComplexityTab,  "  Complexity  "),
            (PerfTab,        "  Performance  "),
        ]:
            tab = cls(nb)
            nb.add(tab, text=label)


# ── Base Tab ──────────────────────────────────────────────────────────────────

class BaseTab(ttk.Frame):
    COLOR = TEXT

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style="TFrame")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=2)
        self._entry = None
        self._info_var = tk.StringVar(value="Size: 0 | Empty: True")
        self._build_canvas()
        self._build_controls_row()
        self._build_log()

    # ── layout builders ──

    def _build_canvas(self):
        self._canvas = tk.Canvas(self, bg=BG2, highlightthickness=1,
                                  highlightbackground=MUTED, height=210)
        self._canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 4))
        self._canvas.bind("<Configure>", lambda _e: self._redraw())

    def _build_controls_row(self):
        outer = tk.Frame(self, bg=BG, pady=6)
        outer.grid(row=1, column=0, sticky="ew", padx=10)

        # value entry
        tk.Label(outer, text="Value:", bg=BG, fg=SUBTEXT,
                 font=("Courier", 11)).pack(side=tk.LEFT, padx=(0, 6))
        self._entry = tk.Entry(
            outer, bg=SURFACE, fg=TEXT, insertbackground=TEXT,
            font=("Courier", 11), relief="flat", width=16,
            highlightthickness=1, highlightbackground=MUTED,
            highlightcolor=self.COLOR
        )
        self._entry.pack(side=tk.LEFT, padx=(0, 14))
        self._entry.bind("<Return>", self._on_enter)

        self._add_buttons(outer)

        # info label on right
        tk.Label(outer, textvariable=self._info_var, bg=BG, fg=SUBTEXT,
                 font=("Courier", 10)).pack(side=tk.RIGHT, padx=8)

    def _build_log(self):
        frame = tk.Frame(self, bg=BG)
        frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(2, 10))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        tk.Label(frame, text="Output Log", bg=BG, fg=SUBTEXT,
                 font=("Courier", 10)).grid(row=0, column=0, sticky="w")

        self._log_box = tk.Text(
            frame, bg=BG2, fg=TEXT, font=("Courier", 10),
            state="disabled", height=8, relief="flat",
            highlightthickness=1, highlightbackground=MUTED
        )
        self._log_box.grid(row=1, column=0, sticky="nsew")

        sb = tk.Scrollbar(frame, bg=MUTED, troughcolor=BG2,
                          command=self._log_box.yview)
        sb.grid(row=1, column=1, sticky="ns")
        self._log_box.configure(yscrollcommand=sb.set)

        self._log_box.tag_configure("ok",   foreground=GREEN)
        self._log_box.tag_configure("err",  foreground=RED)
        self._log_box.tag_configure("info", foreground=YELLOW)
        self._log_box.tag_configure("dim",  foreground=SUBTEXT)

    # ── subclass hooks ──

    def _add_buttons(self, frame):
        raise NotImplementedError

    def _on_enter(self, _event):
        pass

    def _redraw(self):
        raise NotImplementedError

    # ── shared helpers ──

    def _btn(self, parent, text, cmd, color=None):
        c = color or self.COLOR
        b = tk.Button(
            parent, text=text, command=cmd,
            bg=SURFACE, fg=c, font=("Courier", 10, "bold"),
            relief="flat", padx=10, pady=4,
            activebackground=MUTED, activeforeground=c, cursor="hand2",
            bd=0
        )
        b.pack(side=tk.LEFT, padx=3)
        return b

    def _log(self, msg: str, tag: str = "info"):
        self._log_box.configure(state="normal")
        self._log_box.insert("end", f"  {msg}\n", tag)
        self._log_box.see("end")
        self._log_box.configure(state="disabled")

    def _get_val(self, label: str):
        val = self._entry.get().strip()
        if not val:
            self._log(f"✘  Enter a value to {label}.", "err")
            return None
        return val

    def _clear_entry(self):
        self._entry.delete(0, tk.END)

    def _refresh_info(self, ds):
        self._info_var.set(f"Size: {ds.size()} | Empty: {ds.is_empty()}")

    # ── canvas primitives ──

    def _c_rect(self, x1, y1, x2, y2, fill=SURFACE, outline=MUTED, width=2):
        self._canvas.create_rectangle(x1, y1, x2, y2,
                                       fill=fill, outline=outline, width=width)

    def _c_text(self, x, y, text, color=TEXT, size=11, bold=False, anchor="center"):
        self._canvas.create_text(
            x, y, text=text, fill=color, anchor=anchor,
            font=("Courier", size, "bold" if bold else "normal")
        )

    def _c_arrow(self, x1, y, x2):
        self._canvas.create_line(
            x1, y, x2, y, fill=SUBTEXT,
            arrow=tk.LAST, arrowshape=(9, 11, 3), width=2
        )

    def _c_empty(self, text="(empty)"):
        c = self._canvas
        w, h = c.winfo_width() or 400, c.winfo_height() or 200
        self._c_text(w // 2, h // 2, text, SUBTEXT, 11)


# ── Stack Tab ─────────────────────────────────────────────────────────────────

class StackTab(BaseTab):
    COLOR = BLUE

    def __init__(self, parent):
        self._stack = Stack()
        super().__init__(parent)

    def _add_buttons(self, frame):
        self._btn(frame, "Push",  self._push,  BLUE)
        self._btn(frame, "Pop",   self._pop,   RED)
        self._btn(frame, "Peek",  self._peek,  YELLOW)
        self._btn(frame, "Clear", self._clear, SUBTEXT)

    def _on_enter(self, _event):
        self._push()

    def _push(self):
        val = self._get_val("push")
        if val is None:
            return
        self._stack.push(val)
        self._clear_entry()
        self._log(f"✔  Pushed '{val}'", "ok")
        self._refresh_info(self._stack)
        self._redraw()

    def _pop(self):
        try:
            val = self._stack.pop()
            self._log(f"✔  Popped '{val}'", "ok")
        except IndexError as e:
            self._log(f"✘  {e}", "err")
        self._refresh_info(self._stack)
        self._redraw()

    def _peek(self):
        try:
            self._log(f"→  Top element: '{self._stack.peek()}'", "info")
        except IndexError as e:
            self._log(f"✘  {e}", "err")

    def _clear(self):
        self._stack = Stack()
        self._log("·  Stack cleared.", "dim")
        self._refresh_info(self._stack)
        self._redraw()

    def _redraw(self):
        c = self._canvas
        c.delete("all")
        items = self._stack._items
        w, h = c.winfo_width() or 400, c.winfo_height() or 210

        if not items:
            self._c_empty("(empty stack)")
            return

        bw, bh, gap = 130, 38, 5
        x1 = (w - bw) // 2
        max_fit = max(1, (h - 30) // (bh + gap))

        display = list(reversed(items))
        truncated = len(display) > max_fit
        if truncated:
            display = display[:max_fit - 1]

        for i, val in enumerate(display):
            y1 = 16 + i * (bh + gap)
            y2 = y1 + bh
            is_top = (i == 0)
            fill    = BLUE    if is_top else SURFACE
            outline = BLUE    if is_top else MUTED
            text_fg = BG      if is_top else TEXT
            c.create_rectangle(x1, y1, x1 + bw, y2,
                                fill=fill, outline=outline, width=2)
            c.create_text(x1 + bw // 2, (y1 + y2) // 2,
                          text=str(val), fill=text_fg,
                          font=("Courier", 11, "bold"))
            if is_top:
                c.create_text(x1 + bw + 10, (y1 + y2) // 2,
                              text="← TOP", fill=BLUE,
                              font=("Courier", 9), anchor="w")

        if truncated:
            y_dot = 16 + max_fit * (bh + gap) - bh // 2
            c.create_text(x1 + bw // 2, y_dot,
                          text=f"⋯ +{len(items) - max_fit + 1} more",
                          fill=SUBTEXT, font=("Courier", 9))


# ── Queue Tab ─────────────────────────────────────────────────────────────────

class QueueTab(BaseTab):
    COLOR = GREEN

    def __init__(self, parent):
        self._queue = Queue()
        super().__init__(parent)

    def _add_buttons(self, frame):
        self._btn(frame, "Enqueue", self._enqueue, GREEN)
        self._btn(frame, "Dequeue", self._dequeue, RED)
        self._btn(frame, "Peek",    self._peek,    YELLOW)
        self._btn(frame, "Clear",   self._clear,   SUBTEXT)

    def _on_enter(self, _event):
        self._enqueue()

    def _enqueue(self):
        val = self._get_val("enqueue")
        if val is None:
            return
        self._queue.enqueue(val)
        self._clear_entry()
        self._log(f"✔  Enqueued '{val}'", "ok")
        self._refresh_info(self._queue)
        self._redraw()

    def _dequeue(self):
        try:
            val = self._queue.dequeue()
            self._log(f"✔  Dequeued '{val}'", "ok")
        except IndexError as e:
            self._log(f"✘  {e}", "err")
        self._refresh_info(self._queue)
        self._redraw()

    def _peek(self):
        try:
            self._log(f"→  Front element: '{self._queue.peek()}'", "info")
        except IndexError as e:
            self._log(f"✘  {e}", "err")

    def _clear(self):
        self._queue = Queue()
        self._log("·  Queue cleared.", "dim")
        self._refresh_info(self._queue)
        self._redraw()

    def _redraw(self):
        c = self._canvas
        c.delete("all")
        items = list(self._queue._items)
        w, h = c.winfo_width() or 600, c.winfo_height() or 210

        if not items:
            self._c_empty("(empty queue)")
            return

        bw, bh, aw = 76, 46, 24
        max_fit = max(1, (w - 20) // (bw + aw))
        display = items[:max_fit]
        truncated = len(items) > max_fit

        total = len(display) * bw + (len(display) - 1) * aw
        if truncated:
            total += aw + 40  # room for "..." label
        sx = max(12, (w - total) // 2)
        cy = h // 2

        for i, val in enumerate(display):
            x1 = sx + i * (bw + aw)
            x2 = x1 + bw
            y1, y2 = cy - bh // 2, cy + bh // 2
            is_front = (i == 0)
            fill    = GREEN   if is_front else SURFACE
            outline = GREEN   if is_front else MUTED
            text_fg = BG      if is_front else TEXT
            c.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline, width=2)
            c.create_text((x1 + x2) // 2, cy, text=str(val),
                          fill=text_fg, font=("Courier", 11, "bold"))

            label = ""
            label_color = SUBTEXT
            if is_front:
                label, label_color = "FRONT", GREEN
            if i == len(display) - 1 and not truncated:
                label = "REAR" if not is_front else "FRONT / REAR"
                label_color = YELLOW if not is_front else GREEN
            if label:
                c.create_text((x1 + x2) // 2, y1 - 14,
                              text=label, fill=label_color,
                              font=("Courier", 8, "bold"))

            if i < len(display) - 1 or truncated:
                self._c_arrow(x2, cy, x2 + aw)

        if truncated:
            tx = sx + len(display) * (bw + aw)
            c.create_text(tx + 20, cy,
                          text=f"+{len(items) - max_fit}…",
                          fill=SUBTEXT, font=("Courier", 10))


# ── Linked List Tab ───────────────────────────────────────────────────────────

class LinkedListTab(BaseTab):
    COLOR = ORANGE

    def __init__(self, parent):
        self._ll = LinkedList()
        super().__init__(parent)

    def _add_buttons(self, frame):
        self._btn(frame, "Append",  self._append,  ORANGE)
        self._btn(frame, "Prepend", self._prepend, PURPLE)
        self._btn(frame, "Delete",  self._delete,  RED)
        self._btn(frame, "Search",  self._search,  TEAL)
        self._btn(frame, "Clear",   self._clear,   SUBTEXT)

    def _on_enter(self, _event):
        self._append()

    def _append(self):
        val = self._get_val("append")
        if val is None:
            return
        self._ll.append(val)
        self._clear_entry()
        self._log(f"✔  Appended '{val}' to end", "ok")
        self._refresh_info(self._ll)
        self._redraw()

    def _prepend(self):
        val = self._get_val("prepend")
        if val is None:
            return
        self._ll.prepend(val)
        self._clear_entry()
        self._log(f"✔  Prepended '{val}' to front", "ok")
        self._refresh_info(self._ll)
        self._redraw()

    def _delete(self):
        val = self._get_val("delete")
        if val is None:
            return
        try:
            self._ll.delete(val)
            self._clear_entry()
            self._log(f"✔  Deleted '{val}'", "ok")
        except ValueError as e:
            self._log(f"✘  {e}", "err")
        self._refresh_info(self._ll)
        self._redraw()

    def _search(self):
        val = self._get_val("search")
        if val is None:
            return
        if self._ll.search(val):
            self._log(f"✔  '{val}' found in list", "ok")
        else:
            self._log(f"→  '{val}' not found in list", "info")

    def _clear(self):
        self._ll = LinkedList()
        self._log("·  List cleared.", "dim")
        self._refresh_info(self._ll)
        self._redraw()

    def _redraw(self):
        c = self._canvas
        c.delete("all")
        nodes = self._ll.to_list()
        w, h = c.winfo_width() or 600, c.winfo_height() or 210

        if not nodes:
            self._c_empty("(empty list)")
            return

        nw, nh, aw = 72, 46, 30
        null_w = 46
        max_fit = max(1, (w - null_w - 20) // (nw + aw))
        display = nodes[:max_fit]
        truncated = len(nodes) > max_fit

        total = len(display) * nw + len(display) * aw + null_w
        sx = max(12, (w - total) // 2)
        cy = h // 2

        for i, val in enumerate(display):
            x1 = sx + i * (nw + aw)
            x2 = x1 + nw
            y1, y2 = cy - nh // 2, cy + nh // 2
            is_head = (i == 0)
            fill    = ORANGE  if is_head else SURFACE
            outline = ORANGE  if is_head else MUTED
            text_fg = BG      if is_head else TEXT

            c.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline, width=2)
            c.create_text((x1 + x2) // 2, cy, text=str(val),
                          fill=text_fg, font=("Courier", 11, "bold"))
            if is_head:
                c.create_text((x1 + x2) // 2, y1 - 14,
                              text="HEAD", fill=ORANGE, font=("Courier", 8, "bold"))

            self._c_arrow(x2, cy, x2 + aw)

        # None / truncation marker
        last_x2 = sx + len(display) * (nw + aw)
        if truncated:
            c.create_text(last_x2 + null_w // 2, cy,
                          text=f"+{len(nodes) - max_fit}…",
                          fill=SUBTEXT, font=("Courier", 10))
        else:
            c.create_text(last_x2 + null_w // 2, cy,
                          text="None", fill=SUBTEXT,
                          font=("Courier", 10, "italic"))


# ── Complexity Tab ────────────────────────────────────────────────────────────

# Big-O data: (notation, best, worst, explanation)
_COMPLEXITY_DATA = {
    "Stack": {
        "Push (Insert)":  ("O(1)", "O(1)",  "Appends to end of internal list — constant time regardless of size."),
        "Pop (Delete)":   ("O(1)", "O(1)",  "Removes last element of internal list — constant time."),
        "Peek (Access)":  ("O(1)", "O(1)",  "Reads last element by index — no traversal needed."),
        "Search":         ("O(n)", "O(n)",  "Must scan every element top-to-bottom; no random access by value."),
        "Space":          ("O(n)", "O(n)",  "Memory grows linearly with the number of elements stored."),
    },
    "Queue": {
        "Enqueue (Insert)": ("O(1)", "O(1)", "Appends to the tail of a deque — amortized constant time."),
        "Dequeue (Delete)": ("O(1)", "O(1)", "Removes from the head of a deque — constant time."),
        "Peek (Access)":    ("O(1)", "O(1)", "Reads the front element directly — no traversal."),
        "Search":           ("O(n)", "O(n)", "Must scan from front to rear; no index-by-value shortcut."),
        "Space":            ("O(n)", "O(n)", "Memory grows linearly with the number of queued elements."),
    },
    "Linked List": {
        "Prepend (Insert)": ("O(1)", "O(1)", "New node points to old head; head pointer updated in constant time."),
        "Append (Insert)":  ("O(n)", "O(n)", "Must walk every node to reach the tail before inserting."),
        "Delete":           ("O(1)", "O(n)", "Best: deleting the head is O(1). Worst: target is at the tail — full traversal."),
        "Search":           ("O(1)", "O(n)", "Best: target is the head node. Worst: not found or at the tail."),
        "Space":            ("O(n)", "O(n)", "One node object (data + pointer) allocated per element."),
    },
}

_NOTATION_COLORS = {
    "O(1)":      GREEN,
    "O(log n)":  TEAL,
    "O(n)":      YELLOW,
    "O(n log n)": ORANGE,
    "O(n²)":     RED,
}


class ComplexityTab(ttk.Frame):
    """Big-O reference panel for the three project data structures."""

    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        self._detail_var = tk.StringVar(value="Click any cell to see an explanation.")
        self._build()

    def _build(self):
        tk.Label(
            self, text="Big-O Complexity Reference",
            bg=BG, fg=PURPLE, font=("Courier", 13, "bold")
        ).pack(pady=(12, 4))

        tk.Label(
            self,
            text="Color key:  O(1) constant   O(n) linear   Best / Worst shown per operation",
            bg=BG, fg=SUBTEXT, font=("Courier", 9)
        ).pack()

        self._build_legend()
        self._build_table()
        self._build_detail()

    def _build_legend(self):
        row = tk.Frame(self, bg=BG)
        row.pack(pady=(4, 2))
        for notation, color in _NOTATION_COLORS.items():
            tk.Label(row, text=f"  {notation}  ", bg=color, fg=BG,
                     font=("Courier", 9, "bold"), relief="flat", padx=4
                     ).pack(side=tk.LEFT, padx=2)

    def _build_table(self):
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill=tk.BOTH, expand=True, padx=14, pady=(6, 0))

        # Column headers
        headers = ["Operation", "Best", "Worst"]
        col_widths = [22, 10, 10]

        for ds_name, ops in _COMPLEXITY_DATA.items():
            # Section header
            tk.Label(
                outer, text=f"  {ds_name}",
                bg=SURFACE, fg=PURPLE, font=("Courier", 11, "bold"),
                anchor="w", relief="flat"
            ).pack(fill=tk.X, pady=(8, 0))

            frame = tk.Frame(outer, bg=BG)
            frame.pack(fill=tk.X)

            # Header row
            for i, (h, w) in enumerate(zip(headers, col_widths)):
                tk.Label(
                    frame, text=h, bg=MUTED, fg=SUBTEXT,
                    font=("Courier", 9, "bold"), width=w, anchor="w",
                    relief="flat", padx=6, pady=3
                ).grid(row=0, column=i, sticky="ew", padx=1, pady=1)

            # Data rows
            for r, (op_name, (best, worst, explanation)) in enumerate(ops.items(), start=1):
                best_color  = _NOTATION_COLORS.get(best,  TEXT)
                worst_color = _NOTATION_COLORS.get(worst, TEXT)

                op_lbl = tk.Label(
                    frame, text=f"  {op_name}", bg=BG2, fg=TEXT,
                    font=("Courier", 10), width=col_widths[0], anchor="w",
                    relief="flat", padx=6, pady=4, cursor="hand2"
                )
                best_lbl = tk.Label(
                    frame, text=best, bg=best_color, fg=BG,
                    font=("Courier", 10, "bold"), width=col_widths[1], anchor="center",
                    relief="flat", padx=4, pady=4, cursor="hand2"
                )
                worst_lbl = tk.Label(
                    frame, text=worst, bg=worst_color, fg=BG,
                    font=("Courier", 10, "bold"), width=col_widths[2], anchor="center",
                    relief="flat", padx=4, pady=4, cursor="hand2"
                )

                for lbl in (op_lbl, best_lbl, worst_lbl):
                    lbl.bind("<Button-1>", lambda _e, msg=explanation, op=op_name, b=best, w=worst:
                             self._show_detail(op, b, w, msg))
                    lbl.bind("<Enter>", lambda _e, l=op_lbl: l.configure(bg=SURFACE))
                    lbl.bind("<Leave>", lambda _e, l=op_lbl: l.configure(bg=BG2))

                op_lbl.grid(   row=r, column=0, sticky="ew", padx=1, pady=1)
                best_lbl.grid( row=r, column=1, sticky="ew", padx=1, pady=1)
                worst_lbl.grid(row=r, column=2, sticky="ew", padx=1, pady=1)

            frame.columnconfigure(0, weight=3)
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(2, weight=1)

    def _build_detail(self):
        detail_frame = tk.Frame(self, bg=BG2,
                                highlightthickness=1, highlightbackground=MUTED)
        detail_frame.pack(fill=tk.X, padx=14, pady=(8, 12))

        tk.Label(detail_frame, text=" Explanation ", bg=BG2, fg=SUBTEXT,
                 font=("Courier", 9, "bold")).pack(anchor="w", padx=8, pady=(6, 0))
        tk.Label(detail_frame, textvariable=self._detail_var,
                 bg=BG2, fg=TEXT, font=("Courier", 10),
                 wraplength=700, justify="left", anchor="w"
                 ).pack(anchor="w", padx=8, pady=(2, 8))

    def _show_detail(self, op: str, best: str, worst: str, explanation: str):
        self._detail_var.set(f"{op}  —  Best: {best}  |  Worst: {worst}\n{explanation}")


# ── Performance Tab ───────────────────────────────────────────────────────────

# Matplotlib style to match Tokyo Night palette
_MPL_STYLE = {
    "figure.facecolor":  "#1e1e2e",
    "axes.facecolor":    "#181825",
    "axes.edgecolor":    "#45475a",
    "axes.labelcolor":   "#a6adc8",
    "axes.titlecolor":   "#cdd6f4",
    "xtick.color":       "#a6adc8",
    "ytick.color":       "#a6adc8",
    "grid.color":        "#313244",
    "grid.linewidth":    0.6,
    "legend.facecolor":  "#313244",
    "legend.edgecolor":  "#45475a",
    "legend.labelcolor": "#cdd6f4",
    "text.color":        "#cdd6f4",
}

# Per-operation colours (measured line, predicted line)
_OP_PALETTE = [
    ("#7aa2f7", "#7aa2f766"),   # blue
    ("#a6e3a1", "#a6e3a166"),   # green
    ("#fab387", "#fab38766"),   # orange
    ("#cba6f7", "#cba6f766"),   # purple
]

_COMPLEXITY_BADGE = {"O(1)": "#a6e3a1", "O(n)": "#f9e2af"}


class PerfTab(ttk.Frame):
    """Run live benchmarks and display predicted vs. actual Big-O charts."""

    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        self._results = None
        self._running = False
        self._queue = _stdlib_queue.Queue()
        self._build()

    # ── layout ───────────────────────────────────────────────────────────────

    def _build(self):
        # ── top bar ──
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill=tk.X, padx=14, pady=(10, 4))

        tk.Label(bar, text="Performance Benchmark",
                 bg=BG, fg=PURPLE, font=("Courier", 13, "bold")).pack(side=tk.LEFT)

        self._run_btn = tk.Button(
            bar, text="▶  Run Benchmark",
            bg=GREEN, fg=BG, font=("Courier", 10, "bold"),
            relief="flat", padx=12, pady=5,
            activebackground=TEAL, activeforeground=BG, cursor="hand2",
            command=self._start_benchmark,
        )
        self._run_btn.pack(side=tk.RIGHT)

        # ── progress / status ──
        self._status_var = tk.StringVar(
            value="Click  ▶ Run Benchmark  to measure Stack, Queue, and Linked List operations.")
        tk.Label(self, textvariable=self._status_var,
                 bg=BG, fg=SUBTEXT, font=("Courier", 9)
                 ).pack(anchor="w", padx=14)

        self._progress = ttk.Progressbar(self, mode="determinate", maximum=100)
        self._progress.pack(fill=tk.X, padx=14, pady=(2, 6))

        # ── notebook: Charts | Report ──
        self._inner_nb = ttk.Notebook(self)
        self._inner_nb.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 10))

        self._chart_frame  = ttk.Frame(self._inner_nb, style="TFrame")
        self._report_frame = ttk.Frame(self._inner_nb, style="TFrame")
        self._inner_nb.add(self._chart_frame,  text="  Charts  ")
        self._inner_nb.add(self._report_frame, text="  Report  ")

        self._placeholder("Charts will appear here after running the benchmark.",
                          self._chart_frame)
        self._placeholder("The accuracy report will appear here after running the benchmark.",
                          self._report_frame)

    def _placeholder(self, msg: str, parent):
        tk.Label(parent, text=msg, bg=BG, fg=SUBTEXT,
                 font=("Courier", 10)).pack(expand=True)

    # ── benchmark runner ─────────────────────────────────────────────────────

    def _start_benchmark(self):
        if self._running:
            return
        self._running = True
        self._run_btn.configure(state="disabled", text="Running…")
        self._progress["value"] = 0
        threading.Thread(target=self._run_benchmark, daemon=True).start()
        self.after(50, self._poll_queue)

    def _run_benchmark(self):
        def cb(pct, label):
            self._queue.put(("progress", pct, label))

        results = benchmark.run_all(cb)
        self._queue.put(("done", results))

    def _poll_queue(self):
        try:
            while True:
                msg = self._queue.get_nowait()
                if msg[0] == "progress":
                    self._on_progress(msg[1], msg[2])
                elif msg[0] == "done":
                    self._on_done(msg[1])
                    return
        except Exception:
            pass
        if self._running:
            self.after(50, self._poll_queue)

    def _on_progress(self, pct: int, label: str):
        self._progress["value"] = pct
        self._status_var.set(label)

    def _on_done(self, results):
        self._results = results
        self._running = False
        self._run_btn.configure(state="normal", text="▶  Run Again")
        self._status_var.set(
            f"Benchmark complete — {sum(len(r.operations) for r in results)} operations measured "
            f"across {len(benchmark.SIZES)} input sizes.")
        self._draw_charts(results)
        self._draw_report(results)
        self._inner_nb.select(0)

    # ── chart drawing ─────────────────────────────────────────────────────────

    def _draw_charts(self, results):
        for w in self._chart_frame.winfo_children():
            w.destroy()

        with plt.rc_context(_MPL_STYLE):
            fig, axes = plt.subplots(
                1, len(results),
                figsize=(4.6 * len(results), 3.6),
                facecolor=_MPL_STYLE["figure.facecolor"],
            )
            fig.subplots_adjust(left=0.07, right=0.97, top=0.84, bottom=0.14,
                                wspace=0.38)

            if len(results) == 1:
                axes = [axes]

            for ax, ds in zip(axes, results):
                self._plot_ds(ax, ds)

            canvas = FigureCanvasTkAgg(fig, master=self._chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _plot_ds(self, ax, ds):
        sizes_k = [s / 1_000 for s in benchmark.SIZES]

        for i, op in enumerate(ds.operations):
            col_m, col_p = _OP_PALETTE[i % len(_OP_PALETTE)]
            badge = _COMPLEXITY_BADGE.get(op.complexity, TEXT)

            ax.plot(sizes_k, op.times_us,
                    color=col_m, linewidth=2, marker="o", markersize=4,
                    label=f"{op.name} actual")
            ax.plot(sizes_k, op.predicted_us,
                    color=col_p, linewidth=1.5, linestyle="--",
                    label=f"{op.name} predicted ({op.complexity})")

        ax.set_title(ds.ds_name, fontsize=11, fontweight="bold", pad=8)
        ax.set_xlabel("Input size  (×1 000)", fontsize=8)
        ax.set_ylabel("Time  (µs)", fontsize=8)
        ax.grid(True, which="major")
        ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f"))
        ax.tick_params(labelsize=7)
        ax.legend(fontsize=6.5, loc="upper left",
                  framealpha=0.85, handlelength=1.8)

    # ── accuracy report ───────────────────────────────────────────────────────

    def _draw_report(self, results):
        for w in self._report_frame.winfo_children():
            w.destroy()

        outer = tk.Frame(self._report_frame, bg=BG)
        outer.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        tk.Label(outer,
                 text="Prediction Accuracy Report  (mean absolute error between fitted curve and measured time)",
                 bg=BG, fg=SUBTEXT, font=("Courier", 9)
                 ).pack(anchor="w", pady=(0, 6))

        headers = ["Data Structure", "Operation", "Complexity",
                   "Avg Measured (µs)", "Avg Predicted (µs)", "MAE (µs)", "Accuracy"]
        col_w   = [16, 18, 11, 18, 19, 11, 10]

        # header row
        hrow = tk.Frame(outer, bg=MUTED)
        hrow.pack(fill=tk.X)
        for h, w in zip(headers, col_w):
            tk.Label(hrow, text=h, bg=MUTED, fg=SUBTEXT,
                     font=("Courier", 8, "bold"), width=w, anchor="w",
                     relief="flat", padx=4, pady=3
                     ).pack(side=tk.LEFT)

        # data rows
        row_bg = [BG2, BG]
        for ri, ds in enumerate(results):
            for op in ds.operations:
                mae      = self._mae(op.times_us, op.predicted_us)
                avg_m    = sum(op.times_us)    / len(op.times_us)
                avg_p    = sum(op.predicted_us) / len(op.predicted_us)
                accuracy = max(0.0, 1.0 - mae / avg_m) if avg_m > 0 else 1.0
                acc_pct  = f"{accuracy * 100:.1f}%"
                acc_col  = GREEN if accuracy >= 0.85 else (YELLOW if accuracy >= 0.6 else RED)

                bg = row_bg[ri % 2]
                drow = tk.Frame(outer, bg=bg)
                drow.pack(fill=tk.X)

                cells = [
                    (ds.ds_name,          TEXT,     col_w[0]),
                    (op.name,             TEXT,     col_w[1]),
                    (op.complexity,       _COMPLEXITY_BADGE.get(op.complexity, TEXT), col_w[2]),
                    (f"{avg_m:.3f}",      TEXT,     col_w[3]),
                    (f"{avg_p:.3f}",      TEXT,     col_w[4]),
                    (f"{mae:.3f}",        SUBTEXT,  col_w[5]),
                    (acc_pct,             acc_col,  col_w[6]),
                ]
                for val, color, w in cells:
                    tk.Label(drow, text=val, bg=bg, fg=color,
                             font=("Courier", 9), width=w, anchor="w",
                             relief="flat", padx=4, pady=3
                             ).pack(side=tk.LEFT)
                ri += 1

        # legend
        legend = tk.Frame(outer, bg=BG)
        legend.pack(anchor="w", pady=(10, 0))
        tk.Label(legend, text="Accuracy  ", bg=BG, fg=SUBTEXT,
                 font=("Courier", 9)).pack(side=tk.LEFT)
        for label, color in [("≥ 85% good", GREEN), ("≥ 60% fair", YELLOW), ("< 60% poor", RED)]:
            tk.Label(legend, text=f"  {label}  ", bg=color, fg=BG,
                     font=("Courier", 8, "bold"), relief="flat", padx=4
                     ).pack(side=tk.LEFT, padx=2)

    @staticmethod
    def _mae(actual: list[float], predicted: list[float]) -> float:
        return sum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    App().mainloop()
