# Documentation

This directory contains comprehensive documentation for the INQ-ED platform.

---

## Resubmission Notes

- `backend/settings.py` now keeps `DEBUG` opt-in and local-only, so a mixed production host list will not leave debug mode enabled.
- The environment boolean helper now accepts common truthy values such as `true`, `1`, `yes`, and `on`.
- The Django messages framework is now wired through the shared base template, with success messages added for login, logout, registration, profile updates, and class actions.
- Auth regression tests now cover the visible flash-message flow so the feedback remains in place.

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
