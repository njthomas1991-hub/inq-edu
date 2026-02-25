To enable the repository-local git hooks:

1. Make the pre-commit hook executable:

   chmod +x .githooks/pre-commit

2. Tell git to use the `.githooks` directory for hooks (per-repo):

   git config core.hooksPath .githooks

3. Verify by attempting a commit that would include `.env` or a `SECRET_KEY` literal.

Notes:
- The hook file is stored in `.githooks/pre-commit` so it can be committed and shared. After running the two steps above, the hook will run locally for all contributors who enable it.
- If you prefer to install the hook directly into `.git/hooks`, you can copy it instead: `cp .githooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit`.
