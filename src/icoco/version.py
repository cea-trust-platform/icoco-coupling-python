"""Contains version informations."""

from pathlib import Path
from typing import Tuple


def get_version() -> str:
    """Recovers ICoCo package version as string (standard).

    Returns
    -------
    str
        version number as 'x.y.z'.
    """
    return (Path(__file__).parent.resolve() / "VERSION").read_text(encoding="utf-8").strip()


def get_version_int() -> Tuple[int, int, int]:
    """Recovers ICoCo package version as integers.

    Returns
    -------
    Tuple[int, int, int]
        version number as (x, y, z).
    """
    return tuple(int(index) for index in get_version().split('.'))


def get_icoco_version() -> str:
    """Recovers ICoCo version.

    Returns
    -------
    str
        version number as 'x.y'.
    """
    return f"{'.'.join(get_version().split('.')[:2])}"
