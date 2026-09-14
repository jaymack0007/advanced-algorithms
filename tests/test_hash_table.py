import pytest

from src.structures.hash_table import (
    ChainingHashTable,
    OpenAddressHashTable,
)


def test_chaining_insert_and_get():
    table = ChainingHashTable()

    table.insert("a", 1)
    table.insert("b", 2)

    assert table.get("a") == 1
    assert table.get("b") == 2


def test_chaining_update():
    table = ChainingHashTable()

    table.insert("a", 1)
    table.insert("a", 10)

    assert table.get("a") == 10
    assert table.size == 1


def test_chaining_delete():
    table = ChainingHashTable()

    table.insert("a", 1)
    table.delete("a")

    with pytest.raises(KeyError):
        table.get("a")


def test_chaining_rehash():
    table = ChainingHashTable(capacity=4)

    for i in range(10):
        table.insert(i, i * 2)

    assert table.capacity > 4

    for i in range(10):
        assert table.get(i) == i * 2


def test_open_address_insert_and_get():
    table = OpenAddressHashTable()

    table.insert("a", 1)
    table.insert("b", 2)

    assert table.get("a") == 1
    assert table.get("b") == 2


def test_open_address_update():
    table = OpenAddressHashTable()

    table.insert("a", 1)
    table.insert("a", 10)

    assert table.get("a") == 10
    assert table.size == 1


def test_open_address_delete():
    table = OpenAddressHashTable()

    table.insert("a", 1)
    table.delete("a")

    with pytest.raises(KeyError):
        table.get("a")


def test_open_address_rehash():
    table = OpenAddressHashTable(capacity=4)

    for i in range(10):
        table.insert(i, i * 2)

    assert table.capacity > 4

    for i in range(10):
        assert table.get(i) == i * 2


def test_missing_key():
    chaining = ChainingHashTable()
    open_address = OpenAddressHashTable()

    with pytest.raises(KeyError):
        chaining.get("missing")

    with pytest.raises(KeyError):
        open_address.get("missing")