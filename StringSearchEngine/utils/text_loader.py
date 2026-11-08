"""Text-loading and normalization utilities."""

from pathlib import Path
from typing import Dict, Iterable, List


def normalize_text(
    text: str,
    lowercase: bool = False,
    collapse_whitespace: bool = False,
) -> str:
    """Normalize text for search or benchmark input."""
    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string"
        )

    if not isinstance(
        lowercase,
        bool,
    ):
        raise TypeError(
            "lowercase must be boolean"
        )

    if not isinstance(
        collapse_whitespace,
        bool,
    ):
        raise TypeError(
            "collapse_whitespace must be boolean"
        )

    result = text

    if collapse_whitespace:
        result = " ".join(
            result.split()
        )

    if lowercase:
        result = result.lower()

    return result


def _validate_file(
    path: str | Path,
) -> Path:
    """Validate a path that should refer to a readable file."""
    if not isinstance(
        path,
        (str, Path),
    ):
        raise TypeError(
            "path must be a string or Path"
        )

    file_path = Path(
        path
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"file not found: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"path is not a file: {file_path}"
        )

    return file_path


def load_text(
    path: str | Path,
    encoding: str = "utf-8",
    lowercase: bool = False,
    collapse_whitespace: bool = False,
) -> str:
    """Load one text file."""
    if not isinstance(
        encoding,
        str,
    ):
        raise TypeError(
            "encoding must be a string"
        )

    if not encoding:
        raise ValueError(
            "encoding must not be empty"
        )

    file_path = _validate_file(
        path
    )

    text = file_path.read_text(
        encoding=encoding
    )

    return normalize_text(
        text,
        lowercase=lowercase,
        collapse_whitespace=collapse_whitespace,
    )


def load_lines(
    path: str | Path,
    encoding: str = "utf-8",
    skip_empty: bool = False,
) -> List[str]:
    """Load a text file as individual lines without newline characters."""
    if not isinstance(
        skip_empty,
        bool,
    ):
        raise TypeError(
            "skip_empty must be boolean"
        )

    text = load_text(
        path,
        encoding=encoding,
    )

    lines = text.splitlines()

    if skip_empty:
        lines = [
            line
            for line in lines
            if line.strip()
        ]

    return lines


def load_documents(
    paths: Iterable[
        str | Path
    ],
    encoding: str = "utf-8",
    lowercase: bool = False,
    collapse_whitespace: bool = False,
) -> Dict[str, str]:
    """Load several text files into a path-to-content dictionary."""
    if not isinstance(
        paths,
        (list, tuple),
    ):
        raise TypeError(
            "paths must be a list or tuple"
        )

    documents = {}

    for path in paths:
        file_path = _validate_file(
            path
        )

        documents[
            str(
                file_path
            )
        ] = load_text(
            file_path,
            encoding=encoding,
            lowercase=lowercase,
            collapse_whitespace=collapse_whitespace,
        )

    return documents


def file_size_bytes(
    path: str | Path,
) -> int:
    """Return the size of a file in bytes."""
    file_path = _validate_file(
        path
    )

    return file_path.stat().st_size