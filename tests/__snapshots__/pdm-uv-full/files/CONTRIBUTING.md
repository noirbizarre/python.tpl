# Contributing to pdm-uv-example

## Setup

The toolchain is declared in `mise.toml` and pinned in `mise.lock`, so the only
prerequisite is [mise](https://mise.jdx.dev) itself:

```bash
mise install
```

`mise install` wires the prek hooks automatically. When `pdm.lock` exists,
its postinstall hook also installs the project with every dependency group.

A freshly rendered project has no dependency lockfile yet, so create it with:

```bash
pdm install -G:all
```

## The loop

PDM is this project's task host, and the only one. `pdm run --list` shows the
full set with its help strings; mise.toml carries the toolchain and no tasks at
all.

```bash
pdm run test          # the test suite
pdm run cover         # ... with coverage
pdm run lint          # ruff
pdm run format        # ruff, rewriting
pdm run typecheck     # ty
pdm run ci            # everything ♻️ CI runs
```

The other stacks this template renders put the tasks in the other place. That
is deliberate, and there is no shim bridging the two: a `mise run test` that
shelled out to `pdm run test` would give every task two names, two places to
look when it misbehaves, and two chances to go stale against each other.

## Hooks and file style

`prek.toml` uses prek builtins and official upstream hooks. Use `repo = "local"`
only for project-specific checks without an appropriate upstream hook. Run all
hooks with `pdm run hooks`.

`.editorconfig` shares whitespace conventions with editors; its checker leaves
Python to Ruff and Markdown to markdownlint-cli2. Markdown rules and the pretty
output formatter are configured in `.markdownlint-cli2.yaml`.

When updating hook revisions with `prek auto-update`, update the Ruff and ty
minimum versions in `pyproject.toml` alongside them, and run the hooks and CI
tasks together.

## Commits

Conventional Commits, validated on `commit-msg` by `cz check` with the
[emotional](https://github.com/noirbizarre/emotional) rule set. The same rule
set writes `CHANGELOG.md` at release time, so the subject you write is the
changelog entry your users read.

```text
feat(parser): support nested blocks
fix: do not swallow the underlying error
docs: explain the pdm_uv_example entry point
```

`mise run changelog` previews what the unreleased commits would produce.

## Type checking

`ty` runs against Python 3.10, the minimum this package supports,
not against the interpreter you happen to have. A construct that only exists in
a later version is an error here even though it runs fine on your machine —
that is the check working.

## Tests

`tests/`, pytest, `src/` layout. Coverage is reported but not gated locally;
Codecov holds new code to 80%.

## Documentation

```bash
pdm run docs:serve
```

The navigation lives in `zensical.toml`. Every entry must point at a file that
exists — a missing page fails the build, which is deliberate.

## Releasing

Releases are prepared automatically. Every push to `main` runs 🚢 Ship, which
dispatches `prepare-release`; if there are releasable commits it opens or
updates a Release PR titled `chore(release): X` containing the version bump and
the changelog. Review it and merge — the rest is automatic: the merge commit is
tagged, the release is drafted, the artifacts are attached, the
distribution is published to PyPI, and the release is made public.

Do not push to `release/next` by hand; it is moved on every prepare and
anything else on it is discarded.

## This project is generated from a template

It is rendered from [python.tpl](https://github.com/noirbizarre/python.tpl).
When the template moves, 🔄 Template notices within a week:

```bash
pdm run tpl:check     # has it moved?
pdm run tpl:diff      # what would merging it change?
git tpl merge          # take it
```

Anything you add below a `# --- project-specific ---` marker in
`pyproject.toml`, `mise.toml` or `prek.toml` survives that merge. Anything you
change *above* one will conflict, on purpose — those lines are the template's.
