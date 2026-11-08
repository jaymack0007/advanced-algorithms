"""Rolling-hash utilities for Rabin-Karp string matching."""

from dataclasses import dataclass


DEFAULT_BASE = 256
DEFAULT_MODULUS = 1_000_000_007


def _validate_hash_parameters(
    base: int,
    modulus: int,
) -> None:
    """Validate rolling-hash configuration values."""
    if isinstance(
        base,
        bool,
    ) or not isinstance(
        base,
        int,
    ):
        raise TypeError(
            "base must be an integer"
        )

    if isinstance(
        modulus,
        bool,
    ) or not isinstance(
        modulus,
        int,
    ):
        raise TypeError(
            "modulus must be an integer"
        )

    if base <= 0:
        raise ValueError(
            "base must be positive"
        )

    if modulus <= 1:
        raise ValueError(
            "modulus must be greater than 1"
        )


def polynomial_hash(
    text: str,
    base: int = DEFAULT_BASE,
    modulus: int = DEFAULT_MODULUS,
) -> int:
    """
    Compute a polynomial rolling hash for a string.

    Hash recurrence:
        h = (h * base + ord(character)) mod modulus
    """
    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string"
        )

    _validate_hash_parameters(
        base,
        modulus,
    )

    value = 0

    for character in text:
        value = (
            value
            * base
            + ord(
                character
            )
        ) % modulus

    return value


@dataclass
class RollingHash:
    """
    Maintain the hash of a fixed-size sliding string window.

    The current hash can be updated in constant time when one
    character leaves the window and another enters.
    """

    window: str
    base: int = DEFAULT_BASE
    modulus: int = DEFAULT_MODULUS

    def __post_init__(
        self,
    ) -> None:
        if not isinstance(
            self.window,
            str,
        ):
            raise TypeError(
                "window must be a string"
            )

        if not self.window:
            raise ValueError(
                "window must not be empty"
            )

        _validate_hash_parameters(
            self.base,
            self.modulus,
        )

        self.window_size = len(
            self.window
        )

        self.highest_power = pow(
            self.base,
            self.window_size - 1,
            self.modulus,
        )

        self.value = polynomial_hash(
            self.window,
            self.base,
            self.modulus,
        )

    def slide(
        self,
        outgoing: str,
        incoming: str,
    ) -> int:
        """
        Remove one leading character and append one new character.

        Returns the updated hash value.
        """
        if (
            not isinstance(
                outgoing,
                str,
            )
            or len(
                outgoing
            )
            != 1
        ):
            raise ValueError(
                "outgoing must be one character"
            )

        if (
            not isinstance(
                incoming,
                str,
            )
            or len(
                incoming
            )
            != 1
        ):
            raise ValueError(
                "incoming must be one character"
            )

        if outgoing != self.window[
            0
        ]:
            raise ValueError(
                "outgoing character does not match current window"
            )

        reduced = (
            self.value
            - (
                ord(
                    outgoing
                )
                * self.highest_power
            )
        ) % self.modulus

        self.value = (
            reduced
            * self.base
            + ord(
                incoming
            )
        ) % self.modulus

        self.window = (
            self.window[
                1:
            ]
            + incoming
        )

        return self.value

    def matches(
        self,
        candidate: str,
    ) -> bool:
        """Check whether a candidate has the same hash."""
        if not isinstance(
            candidate,
            str,
        ):
            raise TypeError(
                "candidate must be a string"
            )

        if len(
            candidate
        ) != self.window_size:
            return False

        return (
            polynomial_hash(
                candidate,
                self.base,
                self.modulus,
            )
            == self.value
        )