from src.structures.avl_tree import AVLTree


def test_insert_and_search():
    tree = AVLTree()

    for value in [10, 20, 5, 15]:
        tree.insert(value)

    assert tree.search(10)
    assert tree.search(15)
    assert not tree.search(99)


def test_inorder_traversal():
    tree = AVLTree()

    for value in [30, 10, 20, 40, 5]:
        tree.insert(value)

    assert tree.inorder() == [5, 10, 20, 30, 40]


def test_left_rotation():
    tree = AVLTree()

    tree.insert(10)
    tree.insert(20)
    tree.insert(30)

    assert tree.root.key == 20


def test_right_rotation():
    tree = AVLTree()

    tree.insert(30)
    tree.insert(20)
    tree.insert(10)

    assert tree.root.key == 20


def test_double_rotation():
    tree = AVLTree()

    tree.insert(30)
    tree.insert(10)
    tree.insert(20)

    assert tree.root.key == 20


def test_delete():
    tree = AVLTree()

    for value in [20, 10, 30, 5, 15, 25, 35]:
        tree.insert(value)

    tree.delete(30)

    assert not tree.search(30)
    assert tree.inorder() == [5, 10, 15, 20, 25, 35]


def test_tree_height():
    tree = AVLTree()

    for value in [10, 20, 30, 40, 50]:
        tree.insert(value)

    assert tree.height() <= 3


def test_balance_factors():
    tree = AVLTree()

    for value in [50, 40, 30, 20, 10, 25, 35, 45, 60]:
        tree.insert(value)

    def check_balance(node):
        if node is None:
            return

        assert -1 <= node.balance_factor <= 1
        check_balance(node.left)
        check_balance(node.right)

    check_balance(tree.root)