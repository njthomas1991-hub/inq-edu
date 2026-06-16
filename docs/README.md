# Documentation

This directory contains comprehensive documentation for the INQ-ED platform.

---

## Resubmission Notes

### Backend Configuration & Security
- `backend/settings.py` now keeps `DEBUG` opt-in and local-only, so a mixed production host list will not leave debug mode enabled.
- The environment boolean helper now accepts common truthy values such as `true`, `1`, `yes`, and `on`.
- CORS configuration now includes `CORS_ALLOW_CREDENTIALS = True` to allow authenticated frontend-backend communication.
- CSRF_TRUSTED_ORIGINS includes `http://localhost:3000` for local development and testing.

### Frontend Restoration & Integration
- Frontend build system fully restored: `node_modules` packages repaired (`babel-plugin-transform-react-remove-prop-types`, `ajv-keywords`, `caniuse-api`).
- Removed heavy dependency on `pixi.js` for avatar rendering; replaced with lightweight SVG-based `MonsterAvatar` React component.
- Added missing CSS files: `AvatarCustomizer.css` and `MonsterAvatar.css` for proper component styling.
- CRA build and dev server both functional; production build compiles successfully; dev server runs at `http://localhost:3000`.
- Frontend-to-backend API connectivity verified with CORS headers properly configured.

### Django & User Interface
- The Django messages framework is now wired through the shared base template, with success messages added for login, logout, registration, profile updates, and class actions.
- Auth regression tests now cover the visible flash-message flow so the feedback remains in place.
- The Terms of Use, Privacy Policy, and Accessibility Statement pages now render from the existing public templates instead of broken `core/legal/*` paths, which fixed the 500 errors on those routes.
- Both frontend and backend servers run independently on localhost and communicate successfully over CORS-enabled API endpoints.

---

## 📚 Documentation Index

### Core Documentation
- **[Main README](../README.md)** - Complete project documentation and setup guide
- **[Quick Start Guide](../QUICKSTART.md)** - Fast development setup instructions

### System Documentation
- **[DATABASE_SCHEMA_README.md](DATABASE_SCHEMA_README.md)** - Database architecture and table relationships
- **[AVATAR_SYSTEM_README.md](AVATAR_SYSTEM_README.md)** - ClassDojo-style avatar implementation

### Feature Documentation
- **[CANVAS_FEATURES.md](CANVAS_FEATURES.md)** - HTML canvas capabilities for interactive widgets
- **[CANVAS_INTEGRATION_SUMMARY.md](CANVAS_INTEGRATION_SUMMARY.md)** - Canvas integration implementation details
- **[EXPORT_TAB_GUIDE.md](EXPORT_TAB_GUIDE.md)** - Data export functionality documentation

### Administrative Documentation
- **[ADMIN_CREDENTIALS.md](ADMIN_CREDENTIALS.md)** - Admin and teacher demo credentials (development only)
- **[PROJECT_CRITERIA_ASSESSMENT.md](PROJECT_CRITERIA_ASSESSMENT.md)** - Bootcamp project criteria evaluation

---

## 🗂️ Other Documentation Locations

- **Backend Setup**: [../backend/SETUP_HTTPS.md](../backend/SETUP_HTTPS.md)
- **Scripts**: [../scripts/README.md](../scripts/README.md)
- **Frontend**: [../frontend/README.md](../frontend/README.md)

---

## 📝 Document Maintenance

**When to update:**
- After major feature changes
- When database schema changes
- After adding new third-party integrations
- When deployment procedures change

**Style Guide:**
- Use Markdown formatting
- Include code examples where relevant
- Add diagrams for complex systems (Mermaid preferred)
- Keep active links to related documentation
- Version control all documentation changes

---

**Return to:** [Project Root](../) | [Main README](../README.md)
