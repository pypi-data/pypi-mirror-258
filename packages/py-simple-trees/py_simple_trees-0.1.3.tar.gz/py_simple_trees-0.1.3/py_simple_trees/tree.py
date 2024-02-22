from __future__ import annotations

from typing import TypeVar, Generic, Optional
from enum import Enum

from py_simple_trees.node import Node, BinaryNode, AVLNode

K = TypeVar("K")
V = TypeVar("V")

N = TypeVar("N", bound=Node)
BN = TypeVar("BN", bound=BinaryNode)
AVLBN = TypeVar("AVLBN", bound=AVLNode)


class NodeExistedError(RuntimeError):
    ...


class NodeNotExistedError(RuntimeError):
    ...


class NodeTypeNotValidError(RuntimeError):
    ...


class TraversalType(Enum):
    PRE_ORDER = "pre_order"
    IN_ORDER = "in_order"
    POST_ORDER = "post_order"


class GenericTree(Generic[K, V, N]):
    def __init__(self, root: Optional[N] = None):
        self.root: Optional[N] = root

    def insert(self, node: N):
        raise NotImplementedError

    def update(self, node: N):
        raise NotImplementedError

    def search(self, node: N) -> Optional[N]:
        raise NotImplementedError

    def remove(self, node: N):
        raise NotImplementedError

    def traversal(
        self,
        traversal_type: TraversalType = TraversalType.PRE_ORDER,
        reverse: bool = False,
    ):
        if self.root is not None:
            if traversal_type == TraversalType.PRE_ORDER:
                for node in self._pre_order_traversal(self.root, reverse):
                    yield node
            elif traversal_type == TraversalType.IN_ORDER:
                for node in self._in_order_traversal(self.root, reverse):
                    yield node
            elif traversal_type == TraversalType.POST_ORDER:
                for node in self._post_order_traversal(self.root, reverse):
                    yield node

    def _pre_order_traversal(self, node: N, reverse: bool = False):
        pass

    def _in_order_traversal(self, node: N, reverse: bool = False):
        pass

    def _post_order_traversal(self, node: N, reverse: bool = False):
        pass


class BinaryTree(GenericTree[K, V, BN]):
    def __init__(self, root: Optional[BN] = None):
        super().__init__()
        self.root: Optional[BN] = root

    def _pre_order_traversal(self, root: BN, reverse: bool = False):
        yield root
        if not reverse:
            if root.left is not None:
                for node in self._pre_order_traversal(root.left, reverse):
                    yield node
            if root.right is not None:
                for node in self._pre_order_traversal(root.right, reverse):
                    yield node
        else:
            if root.right is not None:
                for node in self._pre_order_traversal(root.right, reverse):
                    yield node
            if root.left is not None:
                for node in self._pre_order_traversal(root.left, reverse):
                    yield node

    def _in_order_traversal(self, root: BN, reverse: bool = False):
        if not reverse:
            if root.left is not None:
                for node in self._in_order_traversal(root.left, reverse):
                    yield node
            yield root
            if root.right is not None:
                for node in self._in_order_traversal(root.right, reverse):
                    yield node
        else:
            if root.right is not None:
                for node in self._in_order_traversal(root.right, reverse):
                    yield node
            yield root
            if root.left is not None:
                for node in self._in_order_traversal(root.left, reverse):
                    yield node

    def _post_order_traversal(self, root: BN, reverse: bool = False):
        if not reverse:
            if root.left is not None:
                for node in self._post_order_traversal(root.left, reverse):
                    yield node
            if root.right is not None:
                for node in self._post_order_traversal(root.right, reverse):
                    yield node
        else:
            if root.right is not None:
                for node in self._post_order_traversal(root.right, reverse):
                    yield node
            if root.left is not None:
                for node in self._post_order_traversal(root.left, reverse):
                    yield node
        yield root

    def remove(self, node: BN):
        return None

    def print(self):
        for node in self.traversal(traversal_type=TraversalType.PRE_ORDER):
            if node.left is not None:
                print(node.key, "--L-->", node.left.key)
            if node.right is not None:
                print(node.key, "--R-->", node.right.key)


class BinarySearchTree(BinaryTree[K, V, BN]):
    def __init__(self):
        super().__init__()

    def insert(self, node: BN):
        if not issubclass(node.__class__, BinaryNode):
            raise NodeTypeNotValidError
        self.root = node if self.root is None else self._insert(self.root, node)

    def _insert(self, root: Optional[BN], node: BN) -> BN:
        if root is None:
            return node
        if node.key < root.key:
            root.left = self._insert(root.left, node)
            return root
        if node.key > root.key:
            root.right = self._insert(root.right, node)
            return root
        raise NodeExistedError

    def update(self, node: BN):
        self.root = self._update(self.root, node)

    def _update(self, root: Optional[BN], node: BN) -> BN:
        if root is None:
            raise NodeNotExistedError
        if node.key < root.key:
            root.left = self._update(root.left, node)
            return root
        elif node.key > root.key:
            root.right = self._update(root.right, node)
            return root
        else:
            return node

    def search(self, node: BN) -> Optional[BN]:
        return self._search(self.root, node)

    def _search(self, root: Optional[BN], node: BN) -> Optional[BN]:
        if root is None:
            return None
        if root.key == node.key:
            return root
        return self._search(root.left, node) or self._search(root.right, node)

    def remove(self, node: BN):
        self.root = self._remove(self.root, node)

    def _remove(self, root: Optional[BN], node: BN) -> Optional[BN]:
        if root is None:
            return None
        if node.key < root.key:
            root.left = self._remove(root.left, node)
            return root
        if node.key > root.key:
            root.right = self._remove(root.right, node)
            return root
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        temp = root.right.min_node
        root.key = temp.key
        root.value = temp.value
        root.right = self._remove(root.right, temp)
        return root


class AVLTree(BinarySearchTree[K, V, AVLBN]):
    def __init__(self):
        super().__init__()

    def insert(self, node: AVLBN):
        if not issubclass(node.__class__, AVLNode):
            raise NodeTypeNotValidError
        self.root = self._insert(self.root, node)

    def _insert(self, root: Optional[AVLBN], node: AVLBN) -> AVLBN:
        if root is None:
            return node
        elif node.key == root.key:
            raise NodeExistedError
        elif node.key < root.key:
            root.left = self._insert(root.left, node)
            root.left_height = 0 if root.left is None else root.left.height
        else:
            root.right = self._insert(root.right, node)
            root.right_height = 0 if root.right is None else root.right.height

        root.height = 1 + max(root.left_height, root.right_height)
        return self._balance(root)

    def remove(self, node: AVLBN):
        self.root = self._remove(self.root, node)

    def _remove(self, root: Optional[AVLBN], node: AVLBN) -> Optional[AVLBN]:
        if root is None:
            return None
        elif node.key < root.key:
            root.left = self._remove(root.left, node)
            root.left_height = 0 if root.left is None else root.left.height
        elif node.key > root.key:
            root.right = self._remove(root.right, node)
            root.right_height = 0 if root.right is None else root.right.height
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = root.right.min_node
            root.key = temp.key
            root.value = temp.value
            root.right = self._remove(root.right, temp)
            root.right_height = 0 if root.right is None else root.right.height

        return self._balance(root)

    def _balance(self, root: AVLBN) -> AVLBN:
        balance_factor = root.balance

        if balance_factor > 1:
            if root.left.balance >= 0:
                return self._right_rotate(root)
            else:
                root.left = self._left_rotate(root.left)
                return self._right_rotate(root)

        if balance_factor < -1:
            if root.right.balance <= 0:
                return self._left_rotate(root)
            else:
                root.right = self._right_rotate(root.right)
                return self._left_rotate(root)

        return root

    # Function to perform left rotation
    def _left_rotate(self, z: AVLBN) -> AVLBN:
        y = z.right
        t2 = y.left
        y.left = z
        z.right = t2

        z.right_height = 0 if t2 is None else t2.height
        z.height = 1 + max(z.left_height, z.right_height)

        y.left_height = z.height
        y.height = 1 + max(y.left_height, y.right_height)

        return y

    # Function to perform right rotation
    def _right_rotate(self, z: AVLBN) -> AVLBN:
        y = z.left
        t3 = y.right
        y.right = z
        z.left = t3

        z.left_height = 0 if t3 is None else t3.height
        z.height = 1 + max(z.left_height, z.right_height)

        y.right_height = z.height
        y.height = 1 + max(y.left_height, y.right_height)

        return y

    def print(self):
        for node in self.traversal(traversal_type=TraversalType.PRE_ORDER):
            if node.left is not None:
                print(node.key, "--L-->", node.left.key)
            if node.right is not None:
                print(node.key, "--R-->", node.right.key)


BSTree = BinarySearchTree
