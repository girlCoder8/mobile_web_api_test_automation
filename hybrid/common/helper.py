from typing import Any, Dict

from hybrid import version as hybrid_version


def library_version() -> str:
    """Return a version of this python library

    Returns:
        str: library version
    """
    return hybrid_version.version
