# Frontend (Vite + React)

This folder contains a minimal Vite + React scaffold intended to live separately from the Django backend.

Quick commands:

```bash
cd frontend
npm install
npm run dev    # local dev server (hot reload)
npm run build  # produce static files into ../static/frontend
```

The production build output is configured to go to `static/frontend` so Django can serve the built assets.
