# Partials

Files here are **not** rendered into a project. They live outside the render
root (`template/`), which is what makes them importable by their
repository-root-relative path from any rendered file:

```jinja
{% import "macros/stack.jinja" as stack %}
{{ stack.install("test") }}
```

They exist for one reason: a child template — `python.fastapi.tpl`,
`python.pytest-plugin.tpl` — that adds a workflow or a section to
`pyproject.toml` must be able to say "install the test group" without knowing
which of the three stacks it is running on. Re-deriving `is_pdm` in the child
is how the child and the parent end up disagreeing about what `pdm-uv` means.

The rule, for this template and its children: **a file body never compares
`stack` directly.** It calls a macro here, or reads a `[computed]` name. There
is exactly one place that knows the stacks apart, and it is not thirty files.

## The one trap

An `{% import %}` binds its alias in the same namespace the answers and
computed values live in. So this:

```jinja
{% import "macros/commands.jinja" as stack %}
```

silently shadows the `stack` answer, and every `{% if stack == 'pdm-uv' %}` in
that file becomes false — comparing a module to a string is not an error, it is
simply never true, and `strict = true` does not catch it because nothing is
undefined.

Import aliases here are therefore chosen to not collide with any question or
computed name: `cmd`, `py`. Check `template.toml` before adding another.

## And one more, in the workflows

`git tpl lint` recognises `{% raw %}` and `{%- raw %}`, but **not**
`{%- raw -%}`. A file that opens with the third form renders correctly and
still gets reported as leaking every `${{ }}` inside it — the render is right
and the lint is wrong, which is the confusing way round.

Every workflow here therefore opens `{%- raw %}name: ...` on one line, which
also removes the blank first line the two-line form leaves behind.
