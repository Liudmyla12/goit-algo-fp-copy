from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Iterable, Tuple


@dataclass
class Node:
    value: int
    next: Optional["Node"] = None


class SinglyLinkedList:
    def __init__(self, values: Iterable[int] = ()) -> None:
        self.head: Optional[Node] = None
        for v in values:
            self.append(v)

    def append(self, value: int) -> None:
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def to_list(self) -> list[int]:
        res = []
        cur = self.head
        while cur:
            res.append(cur.value)
            cur = cur.next
        return res


def reverse_list(head: Optional[Node]) -> Optional[Node]:
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


def _split(head: Node) -> Tuple[Optional[Node], Optional[Node]]:
    slow: Optional[Node] = head
    fast: Optional[Node] = head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next if slow else None
    if slow:
        slow.next = None
    return head, mid


def _merge_sorted(a: Optional[Node], b: Optional[Node]) -> Optional[Node]:
    dummy = Node(0)
    tail = dummy
    while a and b:
        if a.value <= b.value:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a else b
    return dummy.next


def merge_sort(head: Optional[Node]) -> Optional[Node]:
    if head is None or head.next is None:
        return head
    left, right = _split(head)
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)
    return _merge_sorted(left_sorted, right_sorted)


def merge_two_sorted_lists(h1: Optional[Node], h2: Optional[Node]) -> Optional[Node]:
    return _merge_sorted(h1, h2)


def main() -> None:
    ll = SinglyLinkedList([4, 1, 5, 2, 3])
    print("Original:", ll.to_list())

    ll.head = reverse_list(ll.head)
    print("Reversed:", ll.to_list())

    ll.head = merge_sort(ll.head)
    print("Sorted:", ll.to_list())

    a = SinglyLinkedList([1, 3, 5])
    b = SinglyLinkedList([2, 4, 6])
    merged_head = merge_two_sorted_lists(a.head, b.head)
    merged = SinglyLinkedList()
    merged.head = merged_head
    print("Merged sorted:", merged.to_list())


if __name__ == "__main__":
    main()
