RoleRequiredMiddleware

This middleware enforces simple role-based access control using path-prefix mapping.

- File: `quest_app/middleware.py`
- Register in `MIDDLEWARE` (already added after `AuthenticationMiddleware`).

Customize `EXEMPT_PATH_PREFIXES` and `PROTECTED_PATHS` in `quest_app/middleware.py`.

Testing

Run the app tests with:

```bash
python manage.py test quest_app.tests.test_middleware
```

Smoke test

Start the dev server locally:

```bash
python manage.py runserver
```

Then visit protected routes like `/classes/` and `/teacher-resources/` to verify access.
