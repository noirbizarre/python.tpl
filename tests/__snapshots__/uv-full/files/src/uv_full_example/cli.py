"""The `uv-full` command-line interface."""

from __future__ import annotations

import cyclopts

from rich.console import Console
from rich.traceback import install as install_rich_traceback

from uv_full_example import __version__

console = Console()
error_console = Console(stderr=True)

app = cyclopts.App(
    name="uv-full",
    console=console,
    error_console=error_console,
    config=[
        cyclopts.config.Env("UV_FULL_", command=False),
    ],
    help="uv stack, manual release, every slot on",
    version=__version__,
)
install_rich_traceback(console=error_console)


@app.command
def hello(name: str = "world") -> None:
    """Say hello.

    Parameters
    ----------
    name
        Who to greet.
    """
    print(f"Hello, {name}!")
