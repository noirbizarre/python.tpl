"""Assert that a rendered project has exactly one task host.

Run from inside the rendered tree, by `mise run render:check`.

The rule this enforces: a project's tasks live in `[tool.pdm.scripts]` *or* in
mise's `[tasks.*]`, never in both. A delegating `[tasks.test] run = "pdm run
test"` is the tempting middle ground and is the thing being ruled out — it
gives every task two names, two places to look when it misbehaves, and two
chances to go stale against each other.

This cannot be a `git tpl test` assertion: `[expect.contains]` has no negative
form, so "mise.toml defines no tasks" is inexpressible there. Parsing both
files and comparing is a better check than any substring would be anyway — it
sees a task table however it is spelled, including `[tasks.test]`,
`[tasks."docs:build"]` and an inline `tasks = { ... }`.
"""

from __future__ import annotations

import pathlib
import sys
import tomllib

pyproject = tomllib.loads(pathlib.Path("pyproject.toml").read_text())
mise = tomllib.loads(pathlib.Path("mise.toml").read_text())

pdm_scripts = sorted(pyproject.get("tool", {}).get("pdm", {}).get("scripts", {}))
mise_tasks = sorted(mise.get("tasks", {}))

if pdm_scripts and mise_tasks:
    print(
        "two task hosts:\n"
        f"  pyproject.toml [tool.pdm.scripts]: {', '.join(pdm_scripts)}\n"
        f"  mise.toml [tasks]:                 {', '.join(mise_tasks)}\n"
        "\n"
        "A project has one task host. If mise.toml is delegating to PDM, delete\n"
        "the delegations; if PDM has grown a script on the uv stack, move it.",
        file=sys.stderr,
    )
    raise SystemExit(1)

if not pdm_scripts and not mise_tasks:
    print(
        "no task host: neither pyproject.toml nor mise.toml defines any task.",
        file=sys.stderr,
    )
    raise SystemExit(1)

host = "PDM scripts" if pdm_scripts else "mise tasks"
count = len(pdm_scripts or mise_tasks)
print(f"ok — one task host: {host} ({count} tasks)")
