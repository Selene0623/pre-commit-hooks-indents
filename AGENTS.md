# AGENTS.md

Pre-commit hook that converts indents between tabs and spaces. It exposes **two** hooks: `indents-to-tabs` and `indents-to-spaces`. Emitted only for developers of this repo, not end users (see `README.md` for usage).

## Commands

- `make test` — runs `mypy src`, `mypy tests`, then `pytest`. This is the full check before committing. Bootstrap a `.venv` (from `requirements-dev.txt` + `pip install -e .`) if missing; on a fresh clone run `make test` which creates `.venv` and installs deps automatically.
- `make help` — list all targets (`test`, `tox`, `build`, `release`, `clean`, `purge`).
- `pre-commit run --all-files` — repo-wide hooks (black, flake8, isort, prettier, pyupgrade). Config: `.pre-commit-config.yaml`.

## Structure

- src-layout: two sibling packages live in `src/indents_to_tabs/` and `src/indents_to_spaces/`. `setup.cfg` sets `package_dir==src`. Logic and tests are near-identical; the tabs↔spaces difference is the regex in each `convert.py` (`^[ ]+` vs `^[\t]+`).
- Entry point: each package's `main` (`__init__.py`) → `convert_indents` in `convert.py`. Console scripts `indents-to-tabs` / `indents-to-spaces` are registered in `setup.cfg`.
- Tabs tests live in `tests/` reading `tests/testdata/`; spaces tests live in the isolated `tests/spaces/` subdir with its own `testdata/`, because the two share fixture filenames with different content. Keep them separate.
- Version `__version__` lives in each package's `__init__.py`; keep both in sync. `setup.cfg` reads via `attr`.
- `make_indent_replacer` in each `convert.py` converts by `--spaces` chunk (default **4**): adds full units plus leftover chars for exact alignment.

## Gotchas

- Exit codes are inverted from intuition: `PASS = 0`, `FAIL = 1` (`pass_fail_constants.py`, duplicated in each package). The hook returns `FAIL` when it *modified* a file so pre-commit reports the fix. `convert_indents` ORs these together.
- The `--fmt` flag runs a comma-delimited external command (`subprocess.run`) *before* conversion; e.g. `--fmt=terraform,fmt,-write`.
- Working directory: this is a fork of `jambonrose/pre-commit-indents-to-tabs` (remotes: `origin` = Selene0623 fork `pre-commit-hooks-indents`, `upstream` = jambonrose). The spaces package was vendored from `oliv5/pre-commit-indents-to-spaces` (itself derived from upstream PR #1). When updating this fork, be cautious of upstream PRs — a PR titled "Fix typo" may be a full tabs→spaces rebrand reversing one hook's purpose. Review diffs before accepting.