<!-- markdownlint-disable MD013 MD033 -->
<h1 align="center">python.tpl</h1>

<p align="center"><strong>Base stack for Python projects, as a <a href="https://github.com/noirbizarre/git-tpl">git-tpl</a> template</strong></p>

<p align="center">
  <a href="https://github.com/noirbizarre/python.tpl/actions/workflows/render.yaml">
    <img src="https://github.com/noirbizarre/python.tpl/actions/workflows/render.yaml/badge.svg" alt="Render">
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
| Markdown | markdownlint-cli2 with its pretty output formatter |
| Tests | pytest, coverage, `src/` layout |
| Commits & changelog | commitizen with [emotional](https://github.com/noirbizarre/emotional) |
| CI | GitHub Actions: lint, types, a Python matrix |
| License | MIT |

CI and the license are not optional. Everything else is a question.

Hooks prefer prek builtins and official upstream repositories. Local hooks are
reserved for project-specific commands without a suitable upstream hook. Update
Ruff and ty hook revisions together with their dependency minimums so hooks and
project tasks use the same baseline. `.editorconfig` and `.markdownlint-cli2.yaml`
provide shared file-style rules in both this repository and generated projects.

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
`scripts/check-one-task-host.py` fails the render check if either file grows
the other's tasks.

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

## Verification

Three layers, each answering a question the others cannot.

```bash
mise run lint:template          # is this a valid template?
mise run test:template          # does each case render what it should?
mise run render:check uv-full   # is the output a working project?
```

`git tpl lint` catches the two failures that are otherwise silent: a
conditional path segment that renders to a bare extension instead of nothing,
and a GitHub `${{ }}` expression that escaped a `{% raw %}` block. `git tpl
test` runs `tests/*.toml` — and `absent` is the assertion that earns its keep,
because the conditional-path idiom fails by producing a file rather than by
erroring. `render:check` installs the rendered project and runs its own ruff,
ty, pytest and docs build, plus the actual prek hooks (including Markdownlint
and EditorConfig), which is the only layer that would catch a
`pyproject.toml` that renders perfectly and then fails to install.

The cases are also the answer files: `tests/*.toml` is read by `git tpl test`
for `[answers]` and `[expect]`, and by `--answers-from` for `[answers]` alone.
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
