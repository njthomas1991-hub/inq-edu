# Inclusive Quest Education

A Django-based learning platform scaffolded for inclusive educational content and classroom workflows.

## Quick Start (development)

Prerequisites: Python 3.10+ and a virtual environment manager.

1. Create and activate a virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.\.venv\Scripts\Activate  # Windows PowerShell
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment (recommended): create a `.env` file and set `DJANGO_SECRET_KEY`.

4. Run migrations and start the dev server:

```bash
export DJANGO_SECRET_KEY="dev-secret"  # or set in .env
python manage.py migrate
python manage.py runserver
```

5. Create a superuser if needed:

```bash
python manage.py createsuperuser
```

## Project layout

- `inclusive_quest_education/` — Django project settings, urls, wsgi/asgi.
- `quest_app/` — primary application (custom `User` model, views, forms, templates).
- `static/` — static assets (CSS, JS, images).
- `scripts/` — maintenance scripts (admin reset, secret generation, tooling).

## Authentication & User model

- Custom `User` model is defined in `quest_app.models` and uses `username` as `USERNAME_FIELD`.
- Registration flows were fixed to use `User.objects.create_user(...)` so accounts persist correctly.
- `CustomAuthenticationForm` supports email-based login for non-students and includes legacy-account handling.

## Security & Secrets

- Use a `.env` file to store `DJANGO_SECRET_KEY` (see `.env.example` where present). Do not commit `.env`.
- `scripts/generate_secret.py` can produce secure random secrets for local dev.
- Files that may contain credentials are git-ignored (examples: `scripts/set_admin.py`, `scripts/reset_superuser.py`, `.saved_superuser`).

### Admin hardening & history cleanup

- A past commit contained hard-coded admin scripts and credentials. To remediate:
	- A backup branch `backup-before-secret-cleanup` was created.
	- `git-filter-repo` was used to purge sensitive files from the repository history and the cleaned history was force-pushed.
	- Admin management scripts were rewritten to require environment variables (no hard-coded passwords) and `reset_superuser` requires explicit confirmation to run.
	- The `admin` password was rotated during remediation; ensure you rotate any other secrets that may have been exposed earlier.

## Database constraints & migrations

- `Role` choices were moved to module scope in `quest_app/models.py` to avoid import-time errors.
- Model-level validation (`clean()` + `save()`) now validates `User.role` at the application level.
- A DB-level `CheckConstraint` for `User.role` was added in migration `quest_app/migrations/0004_user_role_checkconstraint.py` (allows NULL to preserve existing rows).

To apply migrations locally:

```bash
python manage.py migrate
```

If the migration fails, inspect invalid `role` values and fix them before re-running.

## Admin password locking

- A pre-save signal prevents changing the password for the `admin` username unless the environment variable `ALLOW_ADMIN_PASSWORD_CHANGE=1` is set for the process performing the change. This protects the canonical admin account from accidental or programmatic changes.

## Scripts and maintenance

- `scripts/reset_superuser.py` — safely resets the superuser password (requires `CONFIRM_RESET=1`). By default it writes the new password to `.saved_superuser` (git-ignored) instead of printing it.
- `scripts/set_admin.py` — sets admin password but now requires `ADMIN_PASSWORD` env var; avoid embedding passwords in source.

## Running tests

Run the Django test suite or a subset:

```bash
python manage.py test
python manage.py test quest_app.tests.test_middleware -v 2
```

## Contributing & workflow notes

- After the history rewrite, all collaborators must refresh local clones. Recommended workflow:

```bash
git fetch --all
git reset --hard origin/master
```

- If you have local branches, rebase them onto the rewritten `master` or create fresh branches against `origin/master`.

## Post-cleanup checklist (recommended)

- Rotate any credentials potentially exposed prior to the history purge.
- Verify CI and deployment secrets (update if necessary).
- Notify collaborators about the force-push and migration changes.

## Contact / Support

For workspace-specific maintainer guidance see `.github/copilot-instructions.md` and open issues/PRs for coordination.

---

If you'd like, I can also:
- Create a small script to help collaborators migrate local branches after the rewritten history.
- Generate secure admin credentials and store them in a secure vault or `.saved_superuser` temporarily before removing.



## Recent maintenance & security notes

This section documents recent changes made to the repository to fix authentication issues and to remove accidentally committed secrets from history. It is provided as an operational record for maintainers.

- Registration and authentication fixes:
	- The registration flow in `quest_app` was updated to use `User.objects.create_user(...)` so new users persist correctly.
	- `CustomAuthenticationForm` was improved to allow email-based login for non-student roles and to handle legacy accounts that lacked a username.

- Secrets and secret-key handling:
	- A `.env` approach is recommended for `DJANGO_SECRET_KEY`; a fallback key is generated in development when the env var is missing.
	- A helper script `scripts/generate_secret.py` is included to create secure values.

- Admin credential hardening and history purge:
	- Previously committed scripts contained hard-coded admin credentials (notably `Admin@123`) in `scripts/set_admin_password.py`. These were identified in the repo history.
	- A backup branch `backup-before-secret-cleanup` was created before any history rewriting.
	- `git-filter-repo` was used locally to purge the offending files from repository history (`scripts/set_admin_password.py`, `scripts/set_admin.py`, `set_admin_password.py`, `set_admin.py`). The rewritten history was force-pushed to the remote. Collaborators must re-clone or reset to the new remote history.
	- Admin-management scripts were rewritten to require environment variables (e.g. `ADMIN_PASSWORD`) and a safer `scripts/reset_superuser.py` now requires `CONFIRM_RESET=1` and avoids printing passwords by default.

- Admin password rotation and locking:
	- The `admin` user's password was rotated to a new value and saved temporarily to a git-ignored file named `.saved_superuser` during the rotation process.
	- A pre-save signal was added to `quest_app/models.py` to prevent changing the `admin` password unless the environment variable `ALLOW_ADMIN_PASSWORD_CHANGE=1` is set for the process performing the change.

- Model and DB constraints:
	- `Role` choices were moved to module scope in `quest_app/models.py` to avoid import-time errors.
	- Application-level validation (`clean()` + `save()`) was added to validate `User.role` at the model layer.
	- A DB-level `CheckConstraint` was added in a migration (`quest_app/migrations/0004_user_role_checkconstraint.py`) using `condition=` for Django 6.x compatibility. The constraint allows `NULL` role values to preserve existing rows.

## Post-cleanup actions for maintainers

- Rotate any credentials that may have been exposed before the purge (done for `admin` during maintenance). If you suspect broader compromise, rotate other secrets.
- Inform all collaborators to re-clone the repository due to history rewrite:

```bash
git fetch --all
git reset --hard origin/master
```

- Remove `.saved_superuser` from any local machines where it may exist, verify it is not tracked by Git, and delete it if present.
- Re-apply any local branches that depended on the previous history carefully; prefer creating fresh branches against the rewritten history.

If you want, I can prepare a short script to help users rotate their local branches to the new history or automate notifying collaborators.