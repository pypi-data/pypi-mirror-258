from __future__ import annotations


def test_version() -> None:
    from pypi_changes import __version__

    assert __version__
