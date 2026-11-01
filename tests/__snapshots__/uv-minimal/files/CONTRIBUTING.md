# Contributing to uv-minimal-example

## Setup

The toolchain is declared in `mise.toml` and pinned in `mise.lock`, so the only
prerequisite is [mise](https://mise.jdx.dev) itself:

```bash
mise install
```

`mise install` wires the prek hooks automatically. When `uv.lock` exists,
its postinstall hook also installs the project with every dependency group
and all extras, keeping the lockfile unchanged.

A freshly rendered project has no dependency lockfile yet, so create it with:

```bash
mise run install
```

## The loop

mise is this project's task host, and the only one. `mise tasks` shows the full
set with its descriptions; pyproject.toml has no scripts table and should not
grow one.

```bash
mise run test          # the test suite
mise run cover         # ... with coverage
mise run lint          # ruff
mise run format        # ruff, rewriting
mise run typecheck     # ty
mise run ci            # everything ♻️ CI runs
```

Every task goes through `uv run`, which syncs the environment first — so a task
cannot silently run against a stale `.venv`.

The other stacks this template renders put the tasks in the other place. That
is deliberate, and there is no shim bridging the two: a `mise run test` that
shelled out to `pdm run test` would give every task two names, two places to
look when it misbehaves, and two chances to go stale against each other.

## Hooks and file style

`prek.toml` uses prek builtins and official upstream hooks. Use `repo = "local"`
only for project-specific checks without an appropriate upstream hook. Run all
hooks with `mise run hooks`.

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
docs: explain the uv_minimal_example entry point
```

`mise run changelog` previews what the unreleased commits would produce.

## Type checking

`ty` runs against Python 3.12, the minimum this package supports,
not against the interpreter you happen to have. A construct that only exists in
a later version is an error here even though it runs fine on your machine —
that is the check working.

## Tests

`tests/`, pytest, `src/` layout. Coverage is reported but not gated locally;
the project sets no hard floor.

## Releasing

Releases are prepared automatically. Every push to `main` runs 🚢 Ship, which
dispatches `prepare-release`; if there are releasable commits it opens or
updates a Release PR titled `chore(release): X` containing the version bump and
the changelog. Review it and merge — the rest is automatic: the merge commit is
tagged, the release is drafted, the artifacts are attached, and the release is made public.

Do not push to `release/next` by hand; it is moved on every prepare and
anything else on it is discarded.

## This project is generated from a template

It is rendered from [python.tpl](https://github.com/noirbizarre/python.tpl).
When the template moves, 🔄 Template notices within a week:

```bash
mise run tpl:check     # has it moved?
mise run tpl:diff      # what would merging it change?
git tpl merge          # take it
```

Anything you add below a `# --- project-specific ---` marker in
`pyproject.toml`, `mise.toml` or `prek.toml` survives that merge. Anything you
change *above* one will conflict, on purpose — those lines are the template's.
