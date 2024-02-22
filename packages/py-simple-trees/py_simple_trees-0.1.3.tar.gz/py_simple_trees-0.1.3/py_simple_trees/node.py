from __future__ import annotations

from typing import TypeVar, Generic, Optional, List, Any


K = TypeVar("K")
V = TypeVar("V")


class Node(Generic[K, V]):
    def __init__(self, key: K, value: Optional[V] = None):
        self.key: K = key
        self.value: Optional[V] = value
        self.children: List[Any] = []


class BinaryNode(Node[K, V]):
    def __init__(self, key: K, value: Optional[V] = None):
        super().__init__(key, value)
        self.children: List[BinaryNode | None] = [None, None]

    @property
    def left(self):
        return self.children[0]

    @left.setter
    def left(self, node: Optional[BinaryNode]):
        self.children[0] = node

    @property
    def right(self):
        return self.children[1]

    @right.setter
    def right(self, node: Optional[BinaryNode]):
        self.children[1] = node

    @property
    def min_node(self):
        if self.left is None:
            return self
        return self.left.min_node

    @property
    def max_node(self):
        if self.right is None:
            return self
        return self.right.max_node


class AVLNode(BinaryNode[K, V]):
    def __init__(self, key: K, value: Optional[V] = None):
        super().__init__(key, value)
        self.height = 1
        self.left_height = 0
        self.right_height = 0

    @property
    def balance(self):
        return self.left_height - self.right_height
