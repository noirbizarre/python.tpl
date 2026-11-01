"""PDM with the uv resolver, every slot on"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    # The installed distribution's metadata is the single source of truth,
    # whichever stack wrote it: on this one the version comes from
    # the SCM tag at build time, and metadata is where
    # it lands either way. Reading a `VERSION` file written into the package —
    # what the previous generation of this template did — reports the version of
    # the *source tree*, which stops being the same thing the moment the package
    # is installed from a wheel.
    __version__ = version("pdm-uv-example")
except PackageNotFoundError:  # pragma: no cover - only when running uninstalled
    __version__ = "0.0.0.dev0"

__all__ = ["__version__"]
