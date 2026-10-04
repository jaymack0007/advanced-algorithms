"""Utility functions for bitmask operations."""


def is_city_visited(
    mask: int,
    city: int,
) -> bool:
    """Return whether a city bit is set."""
    return bool(
        mask & (1 << city)
    )


def add_city(
    mask: int,
    city: int,
) -> int:
    """Return a mask with the city added."""
    return (
        mask | (1 << city)
    )


def remove_city(
    mask: int,
    city: int,
) -> int:
    """Return a mask with the city removed."""
    return (
        mask & ~(1 << city)
    )


def visited_cities(
    mask: int,
    city_count: int,
) -> list[int]:
    """Return all city indexes contained in a mask."""
    return [
        city
        for city in range(city_count)
        if is_city_visited(
            mask,
            city,
        )
    ]