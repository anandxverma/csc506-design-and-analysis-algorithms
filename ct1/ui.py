import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from stack import Stack
from queue import Queue
from linked_list import LinkedList

# ── terminal helpers ──────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
RED    = "\033[31m"
BLUE   = "\033[34m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header(title: str, color: str = CYAN):
    width = 54
    bar = "─" * width
    print(f"\n{color}{BOLD}┌{bar}┐{RESET}")
    print(f"{color}{BOLD}│  {title:<{width - 2}}│{RESET}")
    print(f"{color}{BOLD}└{bar}┘{RESET}\n")


def ok(msg: str):
    print(f"  {GREEN}✔  {msg}{RESET}")


def err(msg: str):
    print(f"  {RED}✘  {msg}{RESET}")


def info(msg: str):
    print(f"  {YELLOW}→  {msg}{RESET}")


def prompt(msg: str) -> str:
    return input(f"  {BOLD}{CYAN}>{RESET} {msg}: ").strip()


def section(title: str):
    print(f"\n  {DIM}{'─' * 48}{RESET}")
    print(f"  {BOLD}{title}{RESET}")
    print(f"  {DIM}{'─' * 48}{RESET}")


def pause():
    input(f"\n  {DIM}Press Enter to continue…{RESET}")


# ── visual renderers ──────────────────────────────────────────────────────────

def render_stack(stack: Stack):
    items = stack._items
    if not items:
        print(f"  {DIM}(empty stack){RESET}")
        return
    print()
    print(f"  {DIM}  ┌──────────┐{RESET}  ← top")
    for item in reversed(items):
        print(f"  {CYAN}  │ {str(item):^8} │{RESET}")
        print(f"  {DIM}  ├──────────┤{RESET}")
    print(f"  {DIM}  └──────────┘{RESET}  ← bottom")
    print()


def render_queue(queue: Queue):
    items = list(queue._items)
    if not items:
        print(f"  {DIM}(empty queue){RESET}")
        return
    print()
    front_label = f"  {GREEN}front{RESET}"
    rear_label  = f"  {YELLOW}rear{RESET}"
    cells = "".join(f"{CYAN}┤ {str(i):^6} ├{RESET}" for i in items)
    print(f"  {front_label}  {cells}  {rear_label}")
    print()


def render_linked_list(ll: LinkedList):
    nodes = ll.to_list()
    if not nodes:
        print(f"  {DIM}(empty list){RESET}")
        return
    print()
    parts = [f"{CYAN}[ {v} ]{RESET}" for v in nodes]
    chain = f" {YELLOW}→{RESET} ".join(parts)
    print(f"  {chain}  {YELLOW}→{RESET}  {DIM}None{RESET}")
    print()


# ── per-structure menus ───────────────────────────────────────────────────────

def stack_menu():
    s = Stack()
    ops = [
        ("push  <value>", "push"),
        ("pop          ", "pop"),
        ("peek         ", "peek"),
        ("size / empty ", "info"),
        ("back         ", "back"),
    ]
    while True:
        clear()
        header("Stack  (LIFO)", BLUE)
        render_stack(s)
        section("Operations")
        for i, (label, _) in enumerate(ops, 1):
            print(f"    {BOLD}{i}{RESET}. {label}")
        choice = prompt("\nChoose")
        if choice == "1":
            val = prompt("Value to push")
            s.push(val)
            ok(f"Pushed '{val}'")
        elif choice == "2":
            try:
                val = s.pop()
                ok(f"Popped '{val}'")
            except IndexError as e:
                err(str(e))
        elif choice == "3":
            try:
                ok(f"Top element: '{s.peek()}'")
            except IndexError as e:
                err(str(e))
        elif choice == "4":
            info(f"Size: {s.size()}  |  Empty: {s.is_empty()}")
        elif choice == "5":
            return
        else:
            err("Invalid choice")
        pause()


def queue_menu():
    q = Queue()
    ops = [
        ("enqueue <value>", "enqueue"),
        ("dequeue        ", "dequeue"),
        ("peek           ", "peek"),
        ("size / empty   ", "info"),
        ("back           ", "back"),
    ]
    while True:
        clear()
        header("Queue  (FIFO)", YELLOW)
        render_queue(q)
        section("Operations")
        for i, (label, _) in enumerate(ops, 1):
            print(f"    {BOLD}{i}{RESET}. {label}")
        choice = prompt("\nChoose")
        if choice == "1":
            val = prompt("Value to enqueue")
            q.enqueue(val)
            ok(f"Enqueued '{val}'")
        elif choice == "2":
            try:
                val = q.dequeue()
                ok(f"Dequeued '{val}'")
            except IndexError as e:
                err(str(e))
        elif choice == "3":
            try:
                ok(f"Front element: '{q.peek()}'")
            except IndexError as e:
                err(str(e))
        elif choice == "4":
            info(f"Size: {q.size()}  |  Empty: {q.is_empty()}")
        elif choice == "5":
            return
        else:
            err("Invalid choice")
        pause()


def linked_list_menu():
    ll = LinkedList()
    ops = [
        ("append  <value>", "append"),
        ("prepend <value>", "prepend"),
        ("delete  <value>", "delete"),
        ("search  <value>", "search"),
        ("size / empty   ", "info"),
        ("back           ", "back"),
    ]
    while True:
        clear()
        header("Linked List  (Singly)", GREEN)
        render_linked_list(ll)
        section("Operations")
        for i, (label, _) in enumerate(ops, 1):
            print(f"    {BOLD}{i}{RESET}. {label}")
        choice = prompt("\nChoose")
        if choice == "1":
            val = prompt("Value to append")
            ll.append(val)
            ok(f"Appended '{val}'")
        elif choice == "2":
            val = prompt("Value to prepend")
            ll.prepend(val)
            ok(f"Prepended '{val}'")
        elif choice == "3":
            val = prompt("Value to delete")
            try:
                ll.delete(val)
                ok(f"Deleted '{val}'")
            except ValueError as e:
                err(str(e))
        elif choice == "4":
            val = prompt("Value to search")
            found = ll.search(val)
            if found:
                ok(f"'{val}' found in list")
            else:
                info(f"'{val}' not found in list")
        elif choice == "5":
            info(f"Size: {ll.size()}  |  Empty: {ll.is_empty()}")
        elif choice == "6":
            return
        else:
            err("Invalid choice")
        pause()


# ── main menu ─────────────────────────────────────────────────────────────────

def main():
    while True:
        clear()
        header("Data Structures  —  Interactive Demo", CYAN)
        print(f"  Select a data structure to explore:\n")
        print(f"    {BOLD}1{RESET}.  Stack        (LIFO)")
        print(f"    {BOLD}2{RESET}.  Queue        (FIFO)")
        print(f"    {BOLD}3{RESET}.  Linked List  (singly linked)")
        print(f"    {BOLD}4{RESET}.  Quit\n")
        choice = prompt("Choose")
        if choice == "1":
            stack_menu()
        elif choice == "2":
            queue_menu()
        elif choice == "3":
            linked_list_menu()
        elif choice == "4":
            clear()
            print(f"\n  {DIM}Goodbye.{RESET}\n")
            break
        else:
            err("Invalid choice")
            pause()


if __name__ == "__main__":
    main()
