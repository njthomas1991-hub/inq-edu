Kindlewick frontend — build & deploy

Quick steps to build the Kindlewick app and publish its static files for Django.

Prerequisites
- Node.js (>=16) and npm installed

Local build
1. From the project root run:

```bash
cd frontend/kindlewick_app
npm install
npm run build
```

2. After a successful build the artifacts will be emitted to `static/kindlewick/` (e.g. `static/kindlewick/index.html` and `static/kindlewick/app.js`).

Serve / deploy
- For local Django development, ensure `STATICFILES_DIRS` includes the repo `static/` directory or run `python manage.py collectstatic` before deploy.

CI / Production notes
- Add a CI step to run `npm ci` and `npm run build` in `frontend/kindlewick_app` and commit or copy the output to your static assets directory prior to building the Django image.
- If you change `vite.config.js` base/output settings, update `quest_app/templates/core/kindlewick.html` to point to the correct static path.

Troubleshooting
- If the build fails with unresolved imports, confirm `index.html` points to `./src/main.jsx` (relative path) and that `src/main.jsx` exists.
- If you see caching issues in browsers, update asset filenames or configure cache-busting in Vite.
