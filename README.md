<!-- markdownlint-disable MD013 MD033 -->
<h1 align="center">python.tpl</h1>

<p align="center"><strong>Base stack for Python projects, as a <a href="https://github.com/noirbizarre/git-tpl">git-tpl</a> template</strong></p>

<p align="center">
  <a href="https://github.com/noirbizarre/python.tpl/actions/workflows/ci.yaml">
    <img src="https://github.com/noirbizarre/python.tpl/actions/workflows/ci.yaml/badge.svg" alt="CI">
  </a>
  <img src="https://img.shields.io/github/license/noirbizarre/python.tpl" alt="License">
</p>

<!-- markdownlint-enable MD013 MD033 -->

---

The toolchain, the hooks, the changelog contract and the CI/release workflows
that every Python project here starts from — and nothing above them. There is
no web framework, no ORM and no application shape in this template: those
belong in children that extend it.

```bash
git tpl init https://github.com/noirbizarre/python.tpl my-project
```

## What it renders

| | |
| --- | --- |
| Toolchain | [mise](https://mise.jdx.dev), pinned in `mise.lock` |
| Hooks | [prek](https://github.com/j178/prek), native `prek.toml` |
| Lint & format | [ruff](https://docs.astral.sh/ruff/) |
| Types | [ty](https://github.com/astral-sh/ty) |
| Spelling | [typos](https://github.com/crate-ci/typos) |
| File style | EditorConfig and editorconfig-checker |
| Markdown | [rumdl](https://github.com/rvben/rumdl) |
| Tests | pytest, coverage, `src/` layout |
| Commits & changelog | commitizen with [emotional](https://github.com/noirbizarre/emotional) |
| CI | GitHub Actions: lint, types, a Python matrix |
| License | MIT |

CI and the license are not optional. Everything else is a question.

Hooks prefer prek builtins and official upstream repositories. Local hooks are
reserved for project-specific commands without a suitable upstream hook. Update
Ruff and ty hook revisions together with their dependency minimums so hooks and
project tasks use the same baseline. `.editorconfig` provides shared file-style
rules. Markdown rules live in `.config/rumdl.toml` for this repository and
`[tool.rumdl]` in `pyproject.toml` for generated projects.

## The three stacks

One answer, `stack`, and it reaches exactly six places: the build backend, the
resolver configuration, the task host, the lock-check hook, the workflows'
install step, and where the version lives.

| | `pdm` | `pdm-uv` | `uv` |
| --- | --- | --- | --- |
| Resolver | PDM | uv | uv |
| Backend | `pdm-backend` | `pdm-backend` | `uv_build` |
| Task host | `[tool.pdm.scripts]` | `[tool.pdm.scripts]` | `mise.toml` |
| Lockfile | `pdm.lock` | `pdm.lock` | `uv.lock` |
| Version | the Git tag | the Git tag | `project.version` |

**One task host per project, and no shim between them.** On the PDM stacks
every task is a PDM script — `test`, `ci`, `spell`, `lint:actions`, the `tpl:*`
set — and `mise.toml` carries the toolchain with no `[tasks]` table at all. On
the uv stack it is the other way round.

A delegating `[tasks.test] run = "pdm run test"` is the tempting middle ground
and is exactly what is ruled out: it gives every task two names, two places to
look when it misbehaves, and two chances to go stale against each other.
Rendered snapshots and case expectations pin this task-host split for every
stack.

The workflows never name the host. They call the `task()` macro in
[`macros/commands.jinja`](macros/commands.jinja), which is the only place that
knows which stack puts tasks where.

## The optional slots

`cli` (cyclopts), `docs` (Zensical and mkdocstrings, deployed to GitHub Pages),
`pypi` (Trusted Publishing, no token), `codecov`, and `gh_ship`.

`gh_ship` picks between two genuinely different release shapes rather than
toggling a flag inside one:

- **off** — a single `release.yaml`, dispatched by hand. `need-checks` gates on
  a green CI, then commitizen bumps, tags and releases.
- **on** — the [gh-ship](https://github.com/noirbizarre/gh-ship) Release PR
  flow. `prepare-release` runs `cz bump --files-only` and hands gh-ship a
  `ship.release.json`; merging the Release PR tags, drafts, publishes and makes
  it public.

Commitizen and `emotional` are common to both. Only the orchestration differs.

With `gh_ship` enabled, a single `ship` job runs `gh ship run` to route pushes
and merged Release PRs. `gh_ship_token_mode` selects authentication:

- **`app`** (default) — gh-ship mints and refreshes GitHub App tokens itself.
  The dispatched prepare/publish workflows mint their own App tokens where needed.
- **`token`** — use the optional `SHIP_TOKEN` PAT, falling back to the workflow's
  GitHub token. No App is required. Use a PAT if Release PRs and release-branch
  pushes must trigger CI; GitHub's default token does not trigger those runs.

## Verification

Lint validates the template; tests verify its complete output and exercise the
generated projects.

```bash
mise run lint:template          # validate the template
mise run test:template          # fast expectations and snapshot comparison
mise run test                   # full suite, including generated-project checks
mise run test uv-full           # one case, with all its checks
mise run test:write             # record snapshots for review
```

`git tpl lint` catches the two failures that are otherwise silent: a
conditional path segment that renders to a bare extension instead of nothing,
and a GitHub `${{ }}` expression that escaped a `{% raw %}` block. `git tpl
test` runs `tests/*.toml`: five successful cases compare their complete rendered
file sets, contents and modes against committed `tests/__snapshots__/`. Additional
cases check distribution-name validation and derived package/command defaults,
including invalid-input diagnostic codes. Generated-project commands
install the project and run its Ruff, ty, pytest and optional docs build, plus
configuration validation and actual prek hooks (including rumdl and
EditorConfig). `mise run render:check <case>` also runs a single case.

After an intentional template change, run `mise run test:write`, review the
snapshot diff, and run `mise run test`. Recording only writes snapshots: it
does not run expectations or project commands. Include the updated snapshots
with the template change.

The cases are also the answer files: `tests/*.toml` is read by `git tpl test`
for answers, expectations, snapshots and commands, and by `--answers-from` for
`[answers]` alone.
One file, so the runner and the render tasks cannot drift onto different inputs.

## Extending it

Inheritance is [not yet in git-tpl](https://github.com/noirbizarre/git-tpl), so
this template is built to be ready for it rather than to use it:

- Every stack decision is a `[computed]` name — `is_pdm`, `version_source`,
  `cz` — never an inline comparison in a file body.
- Every per-stack command is a macro in [`macros/`](macros/), outside the
  render root and importable by a child.
- Every file a project extends ends in a `# --- project-specific ---` marker,
  which is also where a child template appends.
- Question names are flat and unnamespaced. There is deliberately no `features`
  multi-choice: it is what made the previous, Copier-based attempt impossible
  to extend.

## License

MIT — see [LICENSE](LICENSE).
