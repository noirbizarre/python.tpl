# Agent notes for full-example

Every optional slot turned on

Read [CONTRIBUTING.md](CONTRIBUTING.md) first; it is written for humans and is
accurate. This file records what is easy to get wrong.

## Commands

Use the tasks, not the underlying tools — they carry the flags CI uses:

```bash
pdm install -G:all  # the environment
pdm run ci          # format:check, lint, typecheck, cover, docs:build
pdm run test -k X   # a subset
pdm run --list      # everything
```

**The task host is PDM, and it is the only one.** `[tool.pdm.scripts]` in
`pyproject.toml` is where every task lives, including `spell`, `lint:actions`
and the `tpl:*` set. `mise.toml` has no `[tasks]` table and must not grow one —
not even a delegation. `mise` here installs the toolchain and nothing more.

## Constraints that are not obvious

- **Python 3.11 is the floor.** `ty` checks against it, and the CI
  matrix runs the tests on it. A construct newer than 3.11 is an
  error even though the development interpreter is 3.14.
- **The supported range is derived, not written down.** `requires-python`, the
  trove classifiers, the ruff `target-version`, the ty environment and the CI
  matrix all come from one answer in the template. Do not edit one of them to
  fix a mismatch — they cannot mismatch, so a mismatch means the file is stale
  and the fix is `git tpl merge`.
- **The version.** It is the Git tag. `pyproject.toml` declares
  `dynamic = ["version"]` and pdm-backend reads the tag at build time. There is
  no version string to edit, and adding one would be a second, divergent
  source of truth.
- **Commit subjects are Conventional Commits**, validated on `commit-msg` and
  used verbatim as changelog entries.
- **`# --- project-specific ---` markers** separate template-owned lines from
  the project's own. Add below the marker. Editing above it means the next
  `git tpl merge` conflicts.

## Where things live

```text
src/full_example/       the package
tests/                   pytest, mirroring src/
docs/                    the documentation site (zensical.toml drives the nav)
.github/workflows/       CI and release
mise.toml                the toolchain — no tasks, by design
pyproject.toml           the package, and the tasks
prek.toml                the hooks — builtins and official upstream repositories
.editorconfig            shared editor and whitespace conventions
.markdownlint-cli2.yaml   Markdown rules and output formatting
```

## Do not

- Add a `.pre-commit-config.yaml`. The hooks live in `prek.toml`; two config
  formats for one runner means one of them is stale.
- Add a second task host. A `[tasks.test]` in `mise.toml` that runs
  `pdm run test` looks
  harmless but gives each task two names and two places to go stale. Keep tasks
  in their stack's single task host.
- Add mypy, black, isort or flake8. ruff and ty cover all four, and running two
  linters means arbitrating between them forever.
- Add a local hook when an official upstream hook exists. Keep Ruff and ty hook
  revisions aligned with their minimum versions in `[dependency-groups]`.
- Commit `.venv`, `src/full_example/VERSION` or
  `coverage.xml`.
