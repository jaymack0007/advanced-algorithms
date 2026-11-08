"""Tests for Week 11 suffix-array and suffix-tree visualization."""

from pathlib import Path

import pytest

from StringSearchEngine.core.suffix_tree import (
    CompressedSuffixTree,
)
from StringSearchEngine.visualization.draw_suffix_tree import (
    draw_suffix_tree,
    tree_to_networkx,
)
from StringSearchEngine.visualization.plot_suffix_array import (
    plot_suffix_array,
    suffix_table,
)


def test_suffix_table_banana():
    rows = suffix_table(
        "banana"
    )

    assert [
        row[
            "start"
        ]
        for row in rows
    ] == [
        5,
        3,
        1,
        0,
        4,
        2,
    ]


def test_suffix_table_contains_suffix_text():
    rows = suffix_table(
        "banana"
    )

    assert rows[
        0
    ][
        "suffix"
    ] == "a"


def test_suffix_table_contains_lcp():
    rows = suffix_table(
        "banana"
    )

    assert [
        row[
            "lcp_next"
        ]
        for row in rows
    ] == [
        1,
        3,
        0,
        0,
        2,
        0,
    ]


def test_suffix_table_empty_text():
    assert suffix_table(
        ""
    ) == []


def test_plot_suffix_array_creates_file(
    tmp_path,
):
    output = (
        tmp_path
        / "suffix_array.png"
    )

    result = plot_suffix_array(
        "banana",
        output,
    )

    assert result == output
    assert output.exists()
    assert output.stat().st_size > 0


def test_plot_suffix_array_creates_parent_directory(
    tmp_path,
):
    output = (
        tmp_path
        / "nested"
        / "suffix_array.png"
    )

    plot_suffix_array(
        "banana",
        output,
    )

    assert output.exists()


def test_tree_to_networkx_has_root():
    tree = CompressedSuffixTree(
        "banana"
    )

    graph = tree_to_networkx(
        tree
    )

    assert 0 in graph.nodes


def test_tree_to_networkx_has_edges():
    tree = CompressedSuffixTree(
        "banana"
    )

    graph = tree_to_networkx(
        tree
    )

    assert graph.number_of_edges() > 0


def test_tree_max_nodes():
    tree = CompressedSuffixTree(
        "banana"
    )

    graph = tree_to_networkx(
        tree,
        max_nodes=4,
    )

    assert graph.number_of_nodes() <= 4


def test_draw_suffix_tree_from_text(
    tmp_path,
):
    output = (
        tmp_path
        / "suffix_tree.png"
    )

    result = draw_suffix_tree(
        "banana",
        output,
    )

    assert result == output
    assert output.exists()
    assert output.stat().st_size > 0


def test_draw_suffix_tree_from_tree(
    tmp_path,
):
    tree = CompressedSuffixTree(
        "banana"
    )

    output = (
        tmp_path
        / "tree.png"
    )

    draw_suffix_tree(
        tree,
        output,
    )

    assert output.exists()


def test_empty_tree_visualization(
    tmp_path,
):
    output = (
        tmp_path
        / "empty_tree.png"
    )

    draw_suffix_tree(
        "",
        output,
    )

    assert output.exists()


def test_nonstring_suffix_table_rejected():
    with pytest.raises(TypeError):
        suffix_table(
            123
        )


def test_invalid_max_suffixes_rejected(
    tmp_path,
):
    with pytest.raises(ValueError):
        plot_suffix_array(
            "banana",
            tmp_path
            / "plot.png",
            max_suffixes=0,
        )


def test_invalid_tree_type_rejected():
    with pytest.raises(TypeError):
        tree_to_networkx(
            "banana"
        )


def test_invalid_tree_max_nodes_rejected():
    tree = CompressedSuffixTree(
        "banana"
    )

    with pytest.raises(ValueError):
        tree_to_networkx(
            tree,
            max_nodes=0,
        )


def test_invalid_draw_input_rejected(
    tmp_path,
):
    with pytest.raises(TypeError):
        draw_suffix_tree(
            123,
            tmp_path
            / "tree.png",
        )