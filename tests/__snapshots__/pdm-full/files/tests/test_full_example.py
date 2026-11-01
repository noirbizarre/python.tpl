from __future__ import annotations

import pytest

import full_example


def test_exposes_a_version() -> None:
    """The package reports the version of the installed distribution.

    Worth a test on its own: `__version__` is read from the distribution
    metadata, so it is the one attribute that fails when the package is
    importable but not actually installed — a state a misconfigured `src`
    layout produces and nothing else in the suite would notice.
    """
    assert full_example.__version__


def test_cli_greets(capsys: pytest.CaptureFixture[str]) -> None:
    """The command runs and writes to stdout.

    Invoked through `app`, the same object `[project.scripts]` points at, so
    this covers the wiring as well as the behaviour. Asserting on the command
    function directly would leave the entry point untested — and the entry
    point is what breaks when the package is renamed.

    `result_action="return_value"` because cyclopts' default action for a
    console script is to call `sys.exit`, which is right for a process and
    wrong for a test.
    """
    from full_example.cli import app

    app(["hello", "--name", "test"], result_action="return_value")

    assert "Hello, test!" in capsys.readouterr().out


def test_cli_environment_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Environment defaults use the CLI namespace; explicit arguments win."""
    from full_example.cli import app

    monkeypatch.setenv("FULL_EXAMPLE_NAME", "environment")

    app(["hello"], result_action="return_value")

    assert "Hello, environment!" in capsys.readouterr().out

    app(["hello", "--name", "argument"], result_action="return_value")

    assert "Hello, argument!" in capsys.readouterr().out
