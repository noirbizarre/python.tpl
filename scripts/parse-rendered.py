"""Parse every TOML and YAML file in a rendered project.

Run from inside the rendered tree, by `mise run render:check`.

This is deliberately not a `git tpl test` assertion. `[expect.contains]` checks
substrings, so it cannot see a stray comma emitted by a conditional, a table
header duplicated across two branches, or a quote left unbalanced in a branch
no other case exercises. A parser can, in about a second, for every file.
"""

from __future__ import annotations

import glob
import pathlib
import sys
import tomllib

import yaml

failures: list[str] = []

for path in sorted(glob.glob("**/*.toml", recursive=True)):
    try:
        tomllib.loads(pathlib.Path(path).read_text())
    except tomllib.TOMLDecodeError as error:
        failures.append(f"{path}: {error}")

for pattern in (".github/**/*.yml", ".github/**/*.yaml"):
    for path in sorted(glob.glob(pattern, recursive=True)):
        try:
            yaml.safe_load(pathlib.Path(path).read_text())
        except yaml.YAMLError as error:
            failures.append(f"{path}: {error}")

if failures:
    for failure in failures:
        print(failure, file=sys.stderr)
    sys.exit(1)

print("ok")
