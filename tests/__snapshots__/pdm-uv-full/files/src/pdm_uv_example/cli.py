"""The `pdm-uv-example` command-line interface."""

from __future__ import annotations

import cyclopts

from rich.console import Console
from rich.traceback import install as install_rich_traceback

from pdm_uv_example import __version__

console = Console()
error_console = Console(stderr=True)

app = cyclopts.App(
    name="pdm-uv-example",
    console=console,
    error_console=error_console,
    config=[
        cyclopts.config.Env("PDM_UV_EXAMPLE_", command=False),
    ],
    help="PDM with the uv resolver, every slot on",
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
