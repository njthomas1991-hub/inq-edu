# Linting & Formatting

This project includes configuration and helper scripts for formatting and linting.

- Config: `pyproject.toml` (Black / isort / Ruff)
- Editor hints: `.editorconfig`
- Helper scripts: `scripts/lint.ps1`, `scripts/lint.sh`
- Dev requirements: `dev-requirements.txt`

Quick start (recommended in a virtualenv):

Windows PowerShell:

```powershell
python -m pip install -r dev-requirements.txt
.
scripts\lint.ps1
```

Unix/macOS:

```bash
python -m pip install -r dev-requirements.txt
./scripts/lint.sh
```

Optional: install `pre-commit` and run `pre-commit install` to run hooks on commit.
