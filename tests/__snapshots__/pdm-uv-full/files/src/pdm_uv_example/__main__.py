"""Entry point for `python -m pdm_uv_example`.

The guard is not ceremony: without it, `from pdm_uv_example.__main__ import app`
— which any documentation tool or test that imports the package tree will do —
runs the CLI as a side effect of the import.
"""

from __future__ import annotations

from pdm_uv_example.cli import app

if __name__ == "__main__":
    app()
