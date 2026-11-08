"""Tests for Week 11 autocomplete."""

import pytest

from StringSearchEngine.applications.autocomplete import (
    AutocompleteEngine,
    AutocompleteSuggestion,
)


def build_engine():
    return AutocompleteEngine(
        [
            (
                "apple",
                10,
            ),
            (
                "application",
                7,
            ),
            (
                "apply",
                5,
            ),
            (
                "banana",
                8,
            ),
            (
                "band",
                4,
            ),
        ]
    )


def test_basic_prefix_search():
    engine = build_engine()

    results = engine.autocomplete(
        "app"
    )

    assert [
        item.term
        for item in results
    ] == [
        "apple",
        "application",
        "apply",
    ]


def test_frequency_ranking():
    engine = build_engine()

    results = engine.autocomplete(
        "app"
    )

    assert [
        item.frequency
        for item in results
    ] == [
        10,
        7,
        5,
    ]


def test_top_k_limit():
    engine = build_engine()

    results = engine.autocomplete(
        "app",
        top_k=2,
    )

    assert len(
        results
    ) == 2


def test_no_matches():
    engine = build_engine()

    assert engine.autocomplete(
        "xyz"
    ) == []


def test_empty_prefix_returns_global_top():
    engine = build_engine()

    results = engine.autocomplete(
        "",
        top_k=3,
    )

    assert [
        item.term
        for item in results
    ] == [
        "apple",
        "banana",
        "application",
    ]


def test_suggestion_type():
    engine = build_engine()

    result = engine.autocomplete(
        "app"
    )[
        0
    ]

    assert isinstance(
        result,
        AutocompleteSuggestion,
    )


def test_default_case_insensitive():
    engine = build_engine()

    assert [
        item.term
        for item in engine.autocomplete(
            "APP"
        )
    ] == [
        "apple",
        "application",
        "apply",
    ]


def test_case_sensitive_mode():
    engine = AutocompleteEngine(
        [
            (
                "Apple",
                5,
            ),
            (
                "apple",
                10,
            ),
        ],
        case_sensitive=True,
    )

    assert [
        item.term
        for item in engine.autocomplete(
            "A"
        )
    ] == [
        "Apple"
    ]


def test_duplicate_terms_merge_frequency():
    engine = AutocompleteEngine(
        [
            (
                "apple",
                3,
            ),
            (
                "apple",
                4,
            ),
        ]
    )

    assert engine.frequency(
        "apple"
    ) == 7


def test_case_insensitive_duplicates_merge():
    engine = AutocompleteEngine(
        [
            (
                "Apple",
                3,
            ),
            (
                "apple",
                4,
            ),
        ]
    )

    assert engine.vocabulary_size() == 1

    assert engine.frequency(
        "APPLE"
    ) == 7


def test_alphabetical_tiebreak():
    engine = AutocompleteEngine(
        [
            (
                "ape",
                5,
            ),
            (
                "apple",
                5,
            ),
            (
                "apricot",
                5,
            ),
        ]
    )

    assert [
        item.term
        for item in engine.autocomplete(
            "a"
        )
    ] == [
        "ape",
        "apple",
        "apricot",
    ]


def test_add_new_term():
    engine = build_engine()

    engine.add(
        "appetite",
        12,
    )

    assert engine.autocomplete(
        "app"
    )[
        0
    ].term == "appetite"


def test_add_existing_term():
    engine = build_engine()

    engine.add(
        "apply",
        10,
    )

    assert engine.frequency(
        "apply"
    ) == 15


def test_record_query():
    engine = build_engine()

    engine.record_query(
        "application",
        5,
    )

    assert engine.frequency(
        "application"
    ) == 12


def test_record_query_changes_ranking():
    engine = build_engine()

    engine.record_query(
        "apply",
        10,
    )

    assert engine.autocomplete(
        "app"
    )[
        0
    ].term == "apply"


def test_frequency_unknown_term():
    engine = build_engine()

    assert engine.frequency(
        "unknown"
    ) == 0


def test_vocabulary_size():
    engine = build_engine()

    assert engine.vocabulary_size() == 5


def test_top_k_zero():
    engine = build_engine()

    assert engine.autocomplete(
        "app",
        top_k=0,
    ) == []


def test_top_k_larger_than_results():
    engine = build_engine()

    results = engine.autocomplete(
        "ban",
        top_k=10,
    )

    assert len(
        results
    ) == 2


def test_exact_term_prefix():
    engine = build_engine()

    results = engine.autocomplete(
        "apple"
    )

    assert [
        item.term
        for item in results
    ] == [
        "apple"
    ]


def test_unicode_terms():
    engine = AutocompleteEngine(
        [
            (
                "café",
                5,
            ),
            (
                "cafeteria",
                3,
            ),
        ]
    )

    assert [
        item.term
        for item in engine.autocomplete(
            "caf"
        )
    ] == [
        "café",
        "cafeteria",
    ]


def test_invalid_terms_container():
    with pytest.raises(TypeError):
        AutocompleteEngine(
            {
                (
                    "apple",
                    1,
                )
            }
        )


def test_invalid_term_entry_type():
    with pytest.raises(TypeError):
        AutocompleteEngine(
            [
                [
                    "apple",
                    1,
                ]
            ]
        )


def test_invalid_term_entry_length():
    with pytest.raises(ValueError):
        AutocompleteEngine(
            [
                (
                    "apple",
                    1,
                    2,
                )
            ]
        )


def test_empty_term_rejected():
    with pytest.raises(ValueError):
        AutocompleteEngine(
            [
                (
                    "",
                    1,
                )
            ]
        )


def test_nonstring_term_rejected():
    with pytest.raises(TypeError):
        AutocompleteEngine(
            [
                (
                    123,
                    1,
                )
            ]
        )


def test_negative_frequency_rejected():
    with pytest.raises(ValueError):
        AutocompleteEngine(
            [
                (
                    "apple",
                    -1,
                )
            ]
        )


def test_noninteger_frequency_rejected():
    with pytest.raises(TypeError):
        AutocompleteEngine(
            [
                (
                    "apple",
                    1.5,
                )
            ]
        )


def test_boolean_frequency_rejected():
    with pytest.raises(TypeError):
        AutocompleteEngine(
            [
                (
                    "apple",
                    True,
                )
            ]
        )


def test_nonstring_prefix_rejected():
    engine = build_engine()

    with pytest.raises(TypeError):
        engine.autocomplete(
            123
        )


def test_negative_top_k_rejected():
    engine = build_engine()

    with pytest.raises(ValueError):
        engine.autocomplete(
            "app",
            top_k=-1,
        )


def test_noninteger_top_k_rejected():
    engine = build_engine()

    with pytest.raises(TypeError):
        engine.autocomplete(
            "app",
            top_k=2.5,
        )


def test_invalid_case_sensitive_rejected():
    with pytest.raises(TypeError):
        AutocompleteEngine(
            [],
            case_sensitive="yes",
        )


def test_frequency_nonstring_rejected():
    engine = build_engine()

    with pytest.raises(TypeError):
        engine.frequency(
            123
        )