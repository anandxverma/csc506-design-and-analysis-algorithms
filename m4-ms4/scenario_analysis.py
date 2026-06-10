"""
Scenario Analysis: Choosing the Right Data Structure
=====================================================
Four real-world scenarios are each implemented with all four data structures
(Stack, Queue, Deque, LinkedList).  After each scenario the output explains
why one structure is the natural fit and what makes the others awkward.

Scenarios
---------
1. Browser Back Button  – STACK is best
2. Printer Queue        – QUEUE is best
3. Browser History with Recycling (bounded history + drop oldest) – DEQUE is best
4. Song Playlist        – LINKED LIST is best
"""

from stack import Stack
from queue import Queue
from deque import Deque
from linked_list import LinkedList

# ── helpers ───────────────────────────────────────────────────────────────────

DIVIDER = "=" * 70
THIN    = "-" * 70


def section(title: str) -> None:
    print(f"\n{DIVIDER}")
    print(f"  SCENARIO: {title}")
    print(DIVIDER)


def sub(label: str) -> None:
    print(f"\n  [{label}]")


def dataset_summary(items: list, label: str, description: str, extras: dict | None = None) -> None:
    print("\n  Dataset Summary:")
    print(f"    Type        : {label}")
    print(f"    Size        : {len(items)} items")
    print(f"    Items       : {items}")
    print(f"    Description : {description}")
    if extras:
        for key, val in extras.items():
            print(f"    {key:<12}: {val}")


def analysis(winner: str, reason: str, tradeoffs: dict[str, str]) -> None:
    print(f"\n{THIN}")
    print(f"  BEST FIT  : {winner}")
    print(f"  WHY       : {reason}")
    print("\n  Why other structures were less efficient:")
    for ds, note in tradeoffs.items():
        print(f"    {ds:<12} — {note}")
    print(THIN)


# ══════════════════════════════════════════════════════════════════════════════
# SCENARIO 1 – Browser Back Button
# ══════════════════════════════════════════════════════════════════════════════
# The user visits pages in order; pressing Back returns to the previous page.
# This is the textbook LIFO pattern: the most-recently visited page is always
# the one we need next.

section("1 – Browser Back Button")

PAGES = ["google.com", "github.com", "docs.python.org", "stackoverflow.com"]
dataset_summary(
    PAGES,
    label="Browser page URLs (strings)",
    description="A sequential list of web pages visited in order. Each Back press should return to the most recently visited page.",
    extras={"Operations": "visit (push), back (pop), current page (peek)"},
)

# ── Stack (best) ──────────────────────────────────────────────────────────────
sub("Stack  ← BEST FIT")
back_stack = Stack()
print("  Visiting pages:")
for page in PAGES:
    back_stack.push(page)
    print(f"    visit  → {page}   |  stack top = {back_stack.peek()}")

print("\n  Pressing Back three times:")
for _ in range(3):
    popped = back_stack.pop()
    current = back_stack.peek() if not back_stack.is_empty() else "(no history)"
    print(f"    back   ← left '{popped}'  |  now on = {current}")

# ── Queue (poor) ──────────────────────────────────────────────────────────────
sub("Queue  ← POOR FIT")
back_q = Queue()
for page in PAGES:
    back_q.enqueue(page)
print("  Queue state:", back_q)
print("  Pressing 'Back' dequeues the FIRST page visited, not the last.")
dequeued = back_q.dequeue()
print(f"  dequeue() returned '{dequeued}'  (should have been '{PAGES[-1]}')")
print("  Result: Back takes you to the oldest page, opposite of what's needed.")

# ── Deque (workable but over-engineered) ──────────────────────────────────────
sub("Deque  ← WORKABLE BUT OVER-ENGINEERED")
back_deq = Deque()
for page in PAGES:
    back_deq.addRear(page)
print("  Deque state:", back_deq)
back_page = back_deq.removeRear()
print(f"  removeRear() = '{back_page}'  ✓ correct page")
print("  Works, but Deque exposes four methods; only addRear/removeRear are used.")
print("  The extra surface area makes intent less clear than a plain Stack.")

# ── Linked List (poor) ────────────────────────────────────────────────────────
sub("Linked List  ← POOR FIT")
back_ll = LinkedList()
for page in PAGES:
    back_ll.insert(page)
back_ll.display()
print("  To simulate Back we must walk to the tail (O(n)), delete it, and")
print("  re-walk to find the new tail — O(n) per Back press with no tail pointer.")

analysis(
    winner="Stack",
    reason=(
        "Back navigation is LIFO: always undo the most-recent action. "
        "push() records a visit in O(1); pop() retrieves the previous page "
        "in O(1).  The intent maps 1-to-1 onto the data structure."
    ),
    tradeoffs={
        "Queue":      "FIFO order returns the oldest page, the exact opposite of Back.",
        "Deque":      "Correct if restricted to one end, but exposes unnecessary operations.",
        "LinkedList": "Tail access requires O(n) traversal; no O(1) peek at the top.",
    },
)


# ══════════════════════════════════════════════════════════════════════════════
# SCENARIO 2 – Printer Queue
# ══════════════════════════════════════════════════════════════════════════════
# Jobs are printed in the order they were submitted — classic FIFO.

section("2 – Printer Queue")

JOBS = ["Report.pdf", "Resume.docx", "Photo.png", "Invoice.pdf"]
dataset_summary(
    JOBS,
    label="Print job filenames (strings)",
    description="A set of documents submitted to a shared printer. Jobs must be processed in submission order (FIFO) to ensure fairness.",
    extras={"Operations": "submit (enqueue), print next (dequeue)"},
)

# ── Queue (best) ──────────────────────────────────────────────────────────────
sub("Queue  ← BEST FIT")
printer_q = Queue()
print("  Submitting jobs:")
for job in JOBS:
    printer_q.enqueue(job)
    print(f"    submit → {job}")

print("\n  Printing jobs:")
while not printer_q.is_empty():
    job = printer_q.dequeue()
    print(f"    print  ← {job}")

# ── Stack (poor) ──────────────────────────────────────────────────────────────
sub("Stack  ← POOR FIT")
printer_s = Stack()
for job in JOBS:
    printer_s.push(job)
print("  Stack state:", printer_s)
print("  Printing jobs in Stack order:")
while not printer_s.is_empty():
    print(f"    print  ← {printer_s.pop()}")
print("  Result: Last submitted job printed first — unfair to earlier submitters.")

# ── Deque (workable but over-engineered) ──────────────────────────────────────
sub("Deque  ← WORKABLE BUT OVER-ENGINEERED")
printer_deq = Deque()
for job in JOBS:
    printer_deq.addRear(job)
print("  Deque state:", printer_deq)
print("  Printing jobs using removeFront:")
while not printer_deq.isEmpty():
    print(f"    print  ← {printer_deq.removeFront()}")
print("  Works, but addFront/removeRear remain unused and invite misuse.")

# ── Linked List (poor) ────────────────────────────────────────────────────────
sub("Linked List  ← POOR FIT")
printer_ll = LinkedList()
for job in JOBS:
    printer_ll.insert(job)
printer_ll.display()
print("  FIFO requires removing from the head (O(1)) and inserting at the tail.")
print("  LinkedList.insert(data) appends to the tail in O(n); no O(1) enqueue.")
print("  A tail-pointer upgrade would help, but that's extra work vs. Queue.")

analysis(
    winner="Queue",
    reason=(
        "Printing is FIFO: first submitted, first printed. "
        "enqueue() adds a job in O(1); dequeue() hands it to the printer "
        "in O(1) (O(n) for a list-backed queue, but conceptually correct). "
        "The semantics perfectly match the real-world expectation."
    ),
    tradeoffs={
        "Stack":      "LIFO order prints the newest job first — violates fairness.",
        "Deque":      "FIFO is achievable but the two extra endpoints add confusion.",
        "LinkedList": "No O(1) tail-append without a tail pointer; more boilerplate needed.",
    },
)


# ══════════════════════════════════════════════════════════════════════════════
# SCENARIO 3 – Browser History with Recycling (bounded, drop oldest)
# ══════════════════════════════════════════════════════════════════════════════
# Store the last N visited pages.  When the history is full, silently drop the
# oldest entry and add the new one at the front (most-recent end).
# The user can scroll forward and backward through recent history.

section("3 – Browser History with Recycling (max 5 pages)")

MAX_HISTORY = 5
VISITED = [
    "google.com", "github.com", "docs.python.org",
    "stackoverflow.com", "reddit.com", "youtube.com", "twitter.com"
]
dataset_summary(
    VISITED,
    label="Browser page URLs (strings)",
    description="A stream of visited pages larger than the history cap. When full, the oldest entry is evicted and the newest is added. Users can also scroll backward and forward.",
    extras={
        "History cap": str(MAX_HISTORY),
        "Operations":  "add newest (addRear), evict oldest (removeFront), scroll back/forward (removeRear/addRear)",
    },
)

# ── Deque (best) ──────────────────────────────────────────────────────────────
sub("Deque  ← BEST FIT")
history_deq = Deque()
print(f"  Visiting {len(VISITED)} pages with a history cap of {MAX_HISTORY}:")
for page in VISITED:
    if history_deq.size() == MAX_HISTORY:
        dropped = history_deq.removeFront()   # drop oldest (front)
        print(f"    history full — dropped oldest: '{dropped}'")
    history_deq.addRear(page)                 # add newest at rear
    print(f"    visit  → {page}  |  {history_deq}")

print("\n  Scrolling backward (removeRear) then forward (addRear):")
current = history_deq.removeRear()
print(f"    back   ← {current}")
prev = history_deq.removeRear()
print(f"    back   ← {prev}  (now viewing '{prev}')")
history_deq.addRear(prev)
history_deq.addRear(current)
print(f"    forward→ {current}  |  {history_deq}")

# ── Stack (poor) ──────────────────────────────────────────────────────────────
sub("Stack  ← POOR FIT")
history_s = Stack()
print("  Using a Stack with manual cap enforcement:")
for page in VISITED:
    history_s.push(page)
    if history_s.size() > MAX_HISTORY:
        # Must rebuild the stack to remove the bottom element — O(n)
        items = []
        while not history_s.is_empty():
            items.append(history_s.pop())
        items = items[:-1]   # drop the oldest (originally at the bottom)
        for item in reversed(items):
            history_s.push(item)
        print(f"    cap exceeded — rebuilt stack to drop oldest (O(n) rebuild)")
    print(f"    visit  → {page}  |  {history_s}")
print("  Dropping the oldest entry requires a full O(n) rebuild of the stack.")

# ── Queue (poor) ──────────────────────────────────────────────────────────────
sub("Queue  ← POOR FIT")
history_q = Queue()
print("  Using a Queue:")
for page in VISITED:
    if history_q.size() == MAX_HISTORY:
        dropped = history_q.dequeue()         # drop oldest from front — O(n)
        print(f"    history full — dropped: '{dropped}'")
    history_q.enqueue(page)
    print(f"    visit  → {page}  |  {history_q}")
print("  Queue can enforce the cap, but scrolling backward means reading from")
print("  the rear — there is no removeRear; the user would need to dequeue")
print("  everything just to reach recent entries.")

# ── Linked List (workable but verbose) ────────────────────────────────────────
sub("Linked List  ← WORKABLE BUT VERBOSE")
history_ll = LinkedList()
print("  Using a LinkedList (insert at head = most recent):")
for page in VISITED:
    history_ll.insert(page, 0)               # O(1) insert at head
    if history_ll.size() > MAX_HISTORY:
        # Must traverse to find and delete the tail node — O(n)
        tail_index = history_ll.size() - 1
        current_node = history_ll._head
        for _ in range(tail_index - 1):
            current_node = current_node.next
        dropped = current_node.next.data
        current_node.next = None
        history_ll._size -= 1
        print(f"    cap exceeded — dropped tail '{dropped}' (O(n) traversal)")
    print(f"    visit  → {page}")
    history_ll.display()
print("  Works, but deleting the tail is O(n) and requires direct node pointer")
print("  manipulation.  With a doubly-linked list it would be O(1), but then")
print("  we have essentially re-implemented a Deque.")

analysis(
    winner="Deque",
    reason=(
        "History needs O(1) access at BOTH ends: addRear to record new visits, "
        "removeFront to recycle the oldest when the cap is hit, and "
        "removeRear/addRear to scroll backward and forward.  Deque is the only "
        "structure that makes all four operations clean and O(1)."
    ),
    tradeoffs={
        "Stack":      "Dropping the oldest entry requires O(n) rebuild; no front access.",
        "Queue":      "Can enforce the cap, but backward scrolling is O(n) or impossible.",
        "LinkedList": "Tail deletion is O(n) without a tail pointer; effectively reimplements Deque.",
    },
)


# ══════════════════════════════════════════════════════════════════════════════
# SCENARIO 4 – Song Playlist
# ══════════════════════════════════════════════════════════════════════════════
# A playlist where songs can be inserted at any position, removed by name,
# reordered by swapping adjacent tracks, and traversed in sequence.

section("4 – Song Playlist")

SONGS = ["Bohemian Rhapsody", "Hotel California", "Stairway to Heaven",
         "Smells Like Teen Spirit", "Imagine"]
dataset_summary(
    SONGS,
    label="Song titles (strings)",
    description="An ordered playlist where songs may be inserted at any position, removed by name, or searched. Mid-list edits are frequent.",
    extras={"Operations": "append, insert at index, delete by value, search by value"},
)

# ── Linked List (best) ────────────────────────────────────────────────────────
sub("Linked List  ← BEST FIT")
playlist_ll = LinkedList()
print("  Building playlist:")
for song in SONGS:
    playlist_ll.insert(song)
playlist_ll.display()

print("\n  Insert 'Purple Haze' after 'Hotel California' (index 2):")
playlist_ll.insert("Purple Haze", 2)
playlist_ll.display()

print("\n  Remove 'Imagine' from the middle of the list:")
playlist_ll.delete("Imagine")
playlist_ll.display()

print("\n  Search for 'Stairway to Heaven':")
idx = playlist_ll.search("Stairway to Heaven")
print(f"    Found at index {idx}")

print(f"\n  Final playlist has {playlist_ll.size()} songs.")

# ── Stack (poor) ──────────────────────────────────────────────────────────────
sub("Stack  ← POOR FIT")
playlist_s = Stack()
for song in SONGS:
    playlist_s.push(song)
print("  Stack state:", playlist_s)
print("  Inserting 'Purple Haze' at position 2 requires popping 3 songs,")
print("  pushing the new one, then pushing the 3 back — O(n) and fragile.")
print("  Deletion of an arbitrary song requires rebuilding the entire stack.")
print("  Only the top song is efficiently accessible.")

# ── Queue (poor) ──────────────────────────────────────────────────────────────
sub("Queue  ← POOR FIT")
playlist_q = Queue()
for song in SONGS:
    playlist_q.enqueue(song)
print("  Queue state:", playlist_q)
print("  Insertion at an arbitrary position requires dequeuing, inserting,")
print("  and re-enqueuing all subsequent songs — O(n) and destructive.")
print("  Removal of a song anywhere except the front is not supported.")

# ── Deque (workable but limited) ──────────────────────────────────────────────
sub("Deque  ← WORKABLE BUT LIMITED")
playlist_deq = Deque()
for song in SONGS:
    playlist_deq.addRear(song)
print("  Deque state:", playlist_deq)
print("  Deque allows O(1) add/remove at both ends (good for next/previous song).")
print("  But inserting or deleting in the middle still requires O(n) shifting")
print("  (because the backing list must shift elements).")
print("  A Deque models a fixed-ends playlist, not a fully editable one.")

analysis(
    winner="Linked List",
    reason=(
        "A playlist is a sequence where any song may be inserted, deleted, or "
        "moved at any position.  LinkedList.insert(song, index) and "
        "LinkedList.delete(song) both work in O(n) but require NO element "
        "shifting — only pointer rewiring.  This is especially valuable for "
        "frequent mid-list edits, and the node structure naturally represents "
        "the 'current song → next song' chain."
    ),
    tradeoffs={
        "Stack":      "Only the top is accessible; mid-list insert/delete requires O(n) rebuild.",
        "Queue":      "Only front/rear operations; arbitrary edits are destructive and O(n).",
        "Deque":      "O(1) at both ends only; mid-list changes still shift all elements.",
    },
)

# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY TABLE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{DIVIDER}")
print("  SUMMARY: Best Data Structure per Scenario")
print(DIVIDER)
rows = [
    ("Scenario",                             "Best Fit",    "Core Access Pattern"),
    ("Browser Back Button",                  "Stack",       "LIFO — always undo the most recent"),
    ("Printer Queue",                        "Queue",       "FIFO — first submitted, first printed"),
    ("Browser History w/ Recycling",         "Deque",       "Both-ends — cap oldest, scroll newest"),
    ("Song Playlist",                        "LinkedList",  "Mid-list insert/delete via pointer rewire"),
]
col_w = [40, 14, 42]
fmt = "  {:<{}} {:<{}} {:<{}}"
print(fmt.format(*[v for pair in zip(rows[0], col_w) for v in pair]))
print(f"  {'-'*col_w[0]} {'-'*col_w[1]} {'-'*col_w[2]}")
for row in rows[1:]:
    print(fmt.format(*[v for pair in zip(row, col_w) for v in pair]))
print()
