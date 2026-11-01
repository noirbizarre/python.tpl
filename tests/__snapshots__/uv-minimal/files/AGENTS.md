# Agent notes for uv-minimal-example

uv stack, gh-ship, nothing else

Read [CONTRIBUTING.md](CONTRIBUTING.md) first; it is written for humans and is
accurate. This file records what is easy to get wrong.

## Commands

Use the tasks, not the underlying tools — they carry the flags CI uses:

```bash
mise run install    # the environment
mise run ci         # format:check, lint, typecheck, cover
mise run test -k X  # a subset
mise tasks          # everything
```

**The task host is mise, and it is the only one.** `[tasks.*]` in `mise.toml`
is where every task lives. `pyproject.toml` has no scripts table and must not
grow one.

Always `mise run <task>`, never bare `mise <task>`: a mise builtin subcommand
of the same name wins silently and says nothing about the task it shadowed.

## Constraints that are not obvious

- **Python 3.12 is the floor.** `ty` checks against it, and the CI
  matrix runs the tests on it. A construct newer than 3.12 is an
  error even though the development interpreter is 3.14.
- **The supported range is derived, not written down.** `requires-python`, the
  trove classifiers, the ruff `target-version`, the ty environment and the CI
  matrix all come from one answer in the template. Do not edit one of them to
  fix a mismatch — they cannot mismatch, so a mismatch means the file is stale
  and the fix is `git tpl merge`.
- **The version.** It is `project.version` in `pyproject.toml`, and
  `cz bump` owns it. Do not edit it by hand; if you do, `uv.lock` is
  immediately stale and the `uv-lock` hook fails the commit.
- **Commit subjects are Conventional Commits**, validated on `commit-msg` and
  used verbatim as changelog entries.
- **`# --- project-specific ---` markers** separate template-owned lines from
  the project's own. Add below the marker. Editing above it means the next
  `git tpl merge` conflicts.

## Where things live

```text
src/uv_minimal_example/       the package
tests/                   pytest, mirroring src/
.github/workflows/       CI and release
mise.toml                the toolchain and the tasks
pyproject.toml           the package
prek.toml                the hooks — builtins and official upstream repositories
.editorconfig            shared editor and whitespace conventions
.markdownlint-cli2.yaml   Markdown rules and output formatting
```

## Do not

- Add a `.pre-commit-config.yaml`. The hooks live in `prek.toml`; two config
  formats for one runner means one of them is stale.
- Add a second task host. A `[tool.pdm.scripts]` table in `pyproject.toml` looks
  harmless but gives each task two names and two places to go stale. Keep tasks
  in their stack's single task host.
- Add mypy, black, isort or flake8. ruff and ty cover all four, and running two
  linters means arbitrating between them forever.
- Add a local hook when an official upstream hook exists. Keep Ruff and ty hook
  revisions aligned with their minimum versions in `[dependency-groups]`.
- Commit `.venv` or
  `coverage.xml`.
