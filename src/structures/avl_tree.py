"""AVL tree implementation."""

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class AVLNode(Generic[T]):
    """Node used by the AVL tree."""

    def __init__(self, key: T):
        self.key = key
        self.left: Optional["AVLNode[T]"] = None
        self.right: Optional["AVLNode[T]"] = None
        self.height = 1
        self.balance_factor = 0


class AVLTree(Generic[T]):
    """Self-balancing binary search tree."""

    def __init__(self):
        self.root: Optional[AVLNode[T]] = None

    def height(self) -> int:
        """Return the height of the tree."""
        return self._height(self.root)

    def _height(self, node: Optional[AVLNode[T]]) -> int:
        if node is None:
            return 0
        return node.height

    def _update(self, node: AVLNode[T]) -> None:
        """Update node height and balance factor."""
        left_height = self._height(node.left)
        right_height = self._height(node.right)

        node.height = 1 + max(left_height, right_height)
        node.balance_factor = left_height - right_height

    def _rotate_right(self, node: AVLNode[T]) -> AVLNode[T]:
        """Perform a right rotation."""
        new_root = node.left
        if new_root is None:
            return node

        moved_subtree = new_root.right

        new_root.right = node
        node.left = moved_subtree

        self._update(node)
        self._update(new_root)

        return new_root

    def _rotate_left(self, node: AVLNode[T]) -> AVLNode[T]:
        """Perform a left rotation."""
        new_root = node.right
        if new_root is None:
            return node

        moved_subtree = new_root.left

        new_root.left = node
        node.right = moved_subtree

        self._update(node)
        self._update(new_root)

        return new_root

    def _rebalance(self, node: AVLNode[T]) -> AVLNode[T]:
        """Rebalance a node when necessary."""
        self._update(node)

        if node.balance_factor > 1:
            if node.left and node.left.balance_factor < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if node.balance_factor < -1:
            if node.right and node.right.balance_factor > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, key: T) -> None:
        """Insert a key into the AVL tree in O(log n) time."""
        self.root = self._insert(self.root, key)

    def _insert(
        self,
        node: Optional[AVLNode[T]],
        key: T,
    ) -> AVLNode[T]:
        if node is None:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node

        return self._rebalance(node)

    def search(self, key: T) -> bool:
        """Return True if the key exists in the tree."""
        current = self.root

        while current is not None:
            if key == current.key:
                return True

            if key < current.key:
                current = current.left
            else:
                current = current.right

        return False

    def delete(self, key: T) -> None:
        """Delete a key and rebalance the AVL tree."""
        self.root = self._delete(self.root, key)

    def _delete(
        self,
        node: Optional[AVLNode[T]],
        key: T,
    ) -> Optional[AVLNode[T]]:
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)

        elif key > node.key:
            node.right = self._delete(node.right, key)

        else:
            if node.left is None:
                return node.right

            if node.right is None:
                return node.left

            successor = self._find_min(node.right)
            node.key = successor.key
            node.right = self._delete(node.right, successor.key)

        return self._rebalance(node)

    def _find_min(self, node: AVLNode[T]) -> AVLNode[T]:
        """Return the smallest node in a subtree."""
        current = node

        while current.left is not None:
            current = current.left

        return current

    def inorder(self) -> List[T]:
        """Return keys using in-order traversal."""
        values: List[T] = []
        self._inorder(self.root, values)
        return values

    def _inorder(
        self,
        node: Optional[AVLNode[T]],
        values: List[T],
    ) -> None:
        if node is None:
            return

        self._inorder(node.left, values)
        values.append(node.key)
        self._inorder(node.right, values)