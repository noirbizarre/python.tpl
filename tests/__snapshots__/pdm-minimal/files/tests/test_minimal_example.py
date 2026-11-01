from __future__ import annotations

import minimal_example


def test_exposes_a_version() -> None:
    """The package reports the version of the installed distribution.

    Worth a test on its own: `__version__` is read from the distribution
    metadata, so it is the one attribute that fails when the package is
    importable but not actually installed — a state a misconfigured `src`
    layout produces and nothing else in the suite would notice.
    """
    assert minimal_example.__version__
