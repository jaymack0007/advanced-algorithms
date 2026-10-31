"""Tests for grayscale image segmentation using graph cuts."""

import pytest

from FlowNetworkSolver.applications.image_seg import (
    SegmentationResult,
    build_segmentation_network,
    segment_grayscale,
)


def test_returns_result_object():
    result = segment_grayscale(
        [
            [
                0,
                255,
            ]
        ],
        foreground_reference=255,
        background_reference=0,
    )

    assert isinstance(
        result,
        SegmentationResult,
    )


def test_dark_and_bright_pixels_separate():
    image = [
        [
            0,
            0,
        ],
        [
            255,
            255,
        ],
    ]

    result = segment_grayscale(
        image,
        foreground_reference=255,
        background_reference=0,
        smoothness=5,
    )

    assert result.mask == [
        [
            0,
            0,
        ],
        [
            1,
            1,
        ],
    ]


def test_single_bright_pixel_is_foreground():
    result = segment_grayscale(
        [
            [
                255
            ]
        ],
        foreground_reference=255,
        background_reference=0,
    )

    assert result.mask == [
        [
            1
        ]
    ]


def test_single_dark_pixel_is_background():
    result = segment_grayscale(
        [
            [
                0
            ]
        ],
        foreground_reference=255,
        background_reference=0,
    )

    assert result.mask == [
        [
            0
        ]
    ]


def test_all_bright_pixels_are_foreground():
    result = segment_grayscale(
        [
            [
                250,
                245,
            ],
            [
                240,
                255,
            ],
        ],
        foreground_reference=255,
        background_reference=0,
    )

    assert result.foreground_pixels == {
        (
            0,
            0,
        ),
        (
            0,
            1,
        ),
        (
            1,
            0,
        ),
        (
            1,
            1,
        ),
    }


def test_all_dark_pixels_are_background():
    result = segment_grayscale(
        [
            [
                0,
                5,
            ],
            [
                10,
                15,
            ],
        ],
        foreground_reference=255,
        background_reference=0,
    )

    assert result.background_pixels == {
        (
            0,
            0,
        ),
        (
            0,
            1,
        ),
        (
            1,
            0,
        ),
        (
            1,
            1,
        ),
    }


def test_every_pixel_receives_one_label():
    image = [
        [
            0,
            100,
            255,
        ],
        [
            20,
            180,
            240,
        ],
    ]

    result = segment_grayscale(
        image,
    )

    all_pixels = (
        result.foreground_pixels
        | result.background_pixels
    )

    assert len(
        all_pixels
    ) == 6

    assert (
        result.foreground_pixels
        & result.background_pixels
    ) == set()


def test_mask_dimensions_match_image():
    image = [
        [
            0,
            50,
            100,
        ],
        [
            150,
            200,
            255,
        ],
    ]

    result = segment_grayscale(
        image
    )

    assert len(
        result.mask
    ) == 2

    assert all(
        len(
            row
        ) == 3
        for row in result.mask
    )


def test_cut_value_matches_max_flow():
    result = segment_grayscale(
        [
            [
                0,
                255,
            ]
        ],
        foreground_reference=255,
        background_reference=0,
    )

    assert result.cut_value == pytest.approx(
        result.max_flow_result.max_flow
    )


def test_network_contains_pixel_nodes():
    (
        network,
        _,
        _,
        _,
    ) = build_segmentation_network(
        [
            [
                0,
                255,
            ],
            [
                50,
                200,
            ],
        ]
    )

    assert (
        0,
        0,
    ) in network.adjacency

    assert (
        1,
        1,
    ) in network.adjacency


def test_network_contains_terminal_nodes():
    (
        network,
        source,
        sink,
        _,
    ) = build_segmentation_network(
        [
            [
                100
            ]
        ]
    )

    assert source in network.adjacency
    assert sink in network.adjacency


def test_nonrectangular_image_rejected():
    with pytest.raises(ValueError):
        segment_grayscale(
            [
                [
                    0,
                    255,
                ],
                [
                    100
                ],
            ]
        )


def test_empty_image_rejected():
    with pytest.raises(ValueError):
        segment_grayscale(
            []
        )


def test_empty_row_rejected():
    with pytest.raises(ValueError):
        segment_grayscale(
            [
                []
            ]
        )


def test_pixel_above_range_rejected():
    with pytest.raises(ValueError):
        segment_grayscale(
            [
                [
                    256
                ]
            ]
        )


def test_negative_pixel_rejected():
    with pytest.raises(ValueError):
        segment_grayscale(
            [
                [
                    -1
                ]
            ]
        )


def test_nonnumeric_pixel_rejected():
    with pytest.raises(TypeError):
        segment_grayscale(
            [
                [
                    "bright"
                ]
            ]
        )


def test_negative_smoothness_rejected():
    with pytest.raises(ValueError):
        segment_grayscale(
            [
                [
                    100
                ]
            ],
            smoothness=-1,
        )


def test_negative_data_weight_rejected():
    with pytest.raises(ValueError):
        segment_grayscale(
            [
                [
                    100
                ]
            ],
            data_weight=-1,
        )