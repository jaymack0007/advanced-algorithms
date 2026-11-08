"""Tests for Week 11 DNA sequence search."""

import pytest

from StringSearchEngine.applications.dna_search import (
    DNASearchResult,
    DNASequenceSearch,
    FASTARecord,
    load_fasta,
    normalize_dna,
    parse_fasta,
    search_fasta_records,
)


def test_normalize_dna_uppercase():
    assert normalize_dna(
        "acgt"
    ) == "ACGT"


def test_normalize_dna_removes_whitespace():
    assert normalize_dna(
        "AC GT\nAC"
    ) == "ACGTAC"


def test_normalize_dna_accepts_n():
    assert normalize_dna(
        "ACNT"
    ) == "ACNT"


def test_invalid_dna_character_rejected():
    with pytest.raises(ValueError):
        normalize_dna(
            "ACGX"
        )


def test_nonstring_dna_rejected():
    with pytest.raises(TypeError):
        normalize_dna(
            123
        )


def test_parse_single_fasta_record():
    records = parse_fasta(
        ">gene1\nACGTACGT"
    )

    assert records == [
        FASTARecord(
            header="gene1",
            sequence="ACGTACGT",
        )
    ]


def test_parse_multiple_fasta_records():
    records = parse_fasta(
        ">gene1\nACGT\n"
        ">gene2\nTTAA"
    )

    assert len(
        records
    ) == 2

    assert records[
        0
    ].header == "gene1"

    assert records[
        1
    ].sequence == "TTAA"


def test_parse_multiline_sequence():
    records = parse_fasta(
        ">gene1\nACGT\nACGT\nAC"
    )

    assert records[
        0
    ].sequence == "ACGTACGTAC"


def test_parse_ignores_blank_lines():
    records = parse_fasta(
        "\n>gene1\n\nACGT\n\n"
    )

    assert records[
        0
    ].sequence == "ACGT"


def test_parse_empty_fasta():
    assert parse_fasta(
        ""
    ) == []


def test_empty_header_rejected():
    with pytest.raises(ValueError):
        parse_fasta(
            ">\nACGT"
        )


def test_sequence_before_header_rejected():
    with pytest.raises(ValueError):
        parse_fasta(
            "ACGT\n>gene1\nACGT"
        )


def test_nonstring_fasta_rejected():
    with pytest.raises(TypeError):
        parse_fasta(
            123
        )


def test_load_fasta(tmp_path):
    path = (
        tmp_path
        / "sample.fasta"
    )

    path.write_text(
        ">gene1\nACGTACGT",
        encoding="utf-8",
    )

    records = load_fasta(
        path
    )

    assert records[
        0
    ].header == "gene1"


def test_missing_fasta_file_rejected(tmp_path):
    with pytest.raises(
        FileNotFoundError
    ):
        load_fasta(
            tmp_path
            / "missing.fasta"
        )


def test_suffix_array_search():
    searcher = DNASequenceSearch(
        "ACGTACGTACGT"
    )

    result = searcher.find(
        "ACGT",
        method="sa",
    )

    assert result.positions == [
        0,
        4,
        8,
    ]


def test_suffix_tree_search():
    searcher = DNASequenceSearch(
        "ACGTACGTACGT"
    )

    result = searcher.find(
        "ACGT",
        method="tree",
    )

    assert result.positions == [
        0,
        4,
        8,
    ]


def test_methods_agree():
    searcher = DNASequenceSearch(
        "GATTACAGATTACA"
    )

    sa_result = searcher.find(
        "TACA",
        method="sa",
    )

    tree_result = searcher.find(
        "TACA",
        method="tree",
    )

    assert (
        sa_result.positions
        == tree_result.positions
    )


def test_result_object():
    searcher = DNASequenceSearch(
        "ACGT"
    )

    result = searcher.find(
        "CG"
    )

    assert isinstance(
        result,
        DNASearchResult,
    )


def test_result_count():
    searcher = DNASequenceSearch(
        "AAAAA"
    )

    result = searcher.find(
        "AAA"
    )

    assert result.count == 3


def test_pattern_normalized():
    searcher = DNASequenceSearch(
        "ACGTACGT"
    )

    result = searcher.find(
        "acgt"
    )

    assert result.pattern == "ACGT"


def test_tree_is_lazy():
    searcher = DNASequenceSearch(
        "ACGTACGT"
    )

    assert searcher._suffix_tree is None


def test_tree_built_after_tree_search():
    searcher = DNASequenceSearch(
        "ACGTACGT"
    )

    searcher.find(
        "ACG",
        method="tree",
    )

    assert searcher._suffix_tree is not None


def test_pattern_not_found():
    searcher = DNASequenceSearch(
        "ACGTACGT"
    )

    assert searcher.find(
        "TTTT"
    ).positions == []


def test_overlapping_dna_matches():
    searcher = DNASequenceSearch(
        "AAAAA"
    )

    assert searcher.find(
        "AAA"
    ).positions == [
        0,
        1,
        2,
    ]


def test_find_many():
    searcher = DNASequenceSearch(
        "ACGTACGT"
    )

    results = searcher.find_many(
        [
            "ACG",
            "CGT",
        ]
    )

    assert results[
        "ACG"
    ].positions == [
        0,
        4,
    ]

    assert results[
        "CGT"
    ].positions == [
        1,
        5,
    ]


def test_find_many_requires_list():
    searcher = DNASequenceSearch(
        "ACGT"
    )

    with pytest.raises(TypeError):
        searcher.find_many(
            (
                "AC",
                "CG",
            )
        )


def test_find_many_rejects_nonstring_pattern():
    searcher = DNASequenceSearch(
        "ACGT"
    )

    with pytest.raises(TypeError):
        searcher.find_many(
            [
                "AC",
                123,
            ]
        )


def test_longest_repeated_sequence_sa():
    searcher = DNASequenceSearch(
        "ACGTACGT"
    )

    assert (
        searcher.longest_repeated_sequence(
            "sa"
        )
        == "ACGT"
    )


def test_longest_repeated_sequence_tree():
    searcher = DNASequenceSearch(
        "ACGTACGT"
    )

    assert (
        searcher.longest_repeated_sequence(
            "tree"
        )
        == "ACGT"
    )


def test_search_fasta_records():
    records = [
        FASTARecord(
            header="gene1",
            sequence="ACGTACGT",
        ),
        FASTARecord(
            header="gene2",
            sequence="TTACGTAA",
        ),
    ]

    results = search_fasta_records(
        records,
        "ACGT",
    )

    assert results[
        "gene1"
    ].positions == [
        0,
        4,
    ]

    assert results[
        "gene2"
    ].positions == [
        2
    ]


def test_search_fasta_records_tree():
    records = [
        FASTARecord(
            header="gene1",
            sequence="AAAAA",
        )
    ]

    results = search_fasta_records(
        records,
        "AAA",
        method="tree",
    )

    assert results[
        "gene1"
    ].positions == [
        0,
        1,
        2,
    ]


def test_invalid_method_rejected():
    searcher = DNASequenceSearch(
        "ACGT"
    )

    with pytest.raises(ValueError):
        searcher.find(
            "AC",
            method="unknown",
        )


def test_nonstring_method_rejected():
    searcher = DNASequenceSearch(
        "ACGT"
    )

    with pytest.raises(TypeError):
        searcher.find(
            "AC",
            method=123,
        )


def test_invalid_record_list_rejected():
    with pytest.raises(TypeError):
        search_fasta_records(
            (
                FASTARecord(
                    header="gene1",
                    sequence="ACGT",
                ),
            ),
            "AC",
        )


def test_invalid_record_object_rejected():
    with pytest.raises(TypeError):
        search_fasta_records(
            [
                "not a record"
            ],
            "AC",
        )