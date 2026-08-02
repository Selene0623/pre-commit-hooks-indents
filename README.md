# Pre-Commit Hook: Convert indents between tabs and spaces

## Usage

This project is intended to be used via
[pre-commit](https://pre-commit.com) and the `.pre-commit-config.yaml`
file.

It ships two hooks:

- `indents-to-tabs` — replaces space indents with tabs
- `indents-to-spaces` — replaces tab indents with spaces

The code below demonstrates a minimal configuration for usage in
`.pre-commit-config.yaml`.

```yaml
- repo: https://github.com/Selene0623/pre-commit-hooks-indents
  rev: v0.0.2
  hooks:
      - id: indents-to-tabs
```

Both hooks accept the same flags:

- `--spaces=INTEGER` — the indent width to convert. Default is `4`.
- `--fmt=COMMAND,ARGS` — run a comma-delimited external command (e.g.
  `terraform fmt -write`) before converting indents.

The configuration below will run the `terraform fmt -write` command
before replacing spaces with tabs in the indents of Terraform files, and
will replace tab indents with spaces in YAML files.

```yaml
- repo: https://github.com/Selene0623/pre-commit-hooks-indents
  rev: v0.0.2
  hooks:
      - id: indents-to-tabs
        args: ["--fmt=terraform,fmt,-write", "--spaces=4"]
        types: ["terraform"]
      - id: indents-to-spaces
        args: ["--fmt=yamlfmt,-d,-yaml.stdout", "--spaces=4"]
        types: ["yaml"]
```

## Project Rationale

This project is a fork of jambonrose's
[pre-commit-indents-to-tabs](https://github.com/jambonrose/pre-commit-indents-to-tabs),
extended to replace *either* direction of indentation, so teams that
prefer spaces and teams that prefer tabs can both use it from a single
repo.

Philosophically speaking: Tabs are for indents. Spaces are for
alignment. Tabs allow people to set their own preference, a necessity
for those with different needs.