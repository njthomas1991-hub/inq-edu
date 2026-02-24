# Inclusive Quest Education

This project is a modern Django web application scaffolded for inclusive educational tools and workflows.

## Features
- Django 6.x project structure
- Initial app: quest_app
- Ready for further customization

## Setup
1. Create a virtual environment and activate it.
2. Install dependencies from requirements.txt.
3. Run migrations and start the development server.

## Development
- Follow Django best practices.
- Update requirements.txt as needed.
- Add new apps and features as required.

---

For workspace-specific instructions, see .github/copilot-instructions.md.

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