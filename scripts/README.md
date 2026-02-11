# Utility Scripts

This directory contains utility scripts for database management, admin operations, and testing.

> **⚠️ Note:** These scripts are for development/debugging purposes only. Do not use in production.

---

## Database Management

### `add_column.py`
**Purpose:** Add columns to existing database tables  
**Usage:** `python scripts/add_column.py`  
**When to use:** Manual schema modifications outside of migrations

### `check_columns.py`
**Purpose:** Verify database column structure  
**Usage:** `python scripts/check_columns.py`  
**When to use:** Debugging schema issues

### `fix_db.py`
**Purpose:** Fix common database issues  
**Usage:** `python scripts/fix_db.py`  
**When to use:** Resolve migration conflicts or data corruption

### `check_and_migrate.py`
**Purpose:** Check database state and run migrations  
**Usage:** `python scripts/check_and_migrate.py`  
**When to use:** Deployment or after pulling new migrations

### `check_avatar_table.py`
**Purpose:** Verify Avatar table structure  
**Usage:** `python scripts/check_avatar_table.py`  
**When to use:** Debugging avatar system issues

### `create_analytics_table.py`
**Purpose:** Create SchoolAnalyticsProfile table  
**Usage:** `python scripts/create_analytics_table.py`  
**When to use:** Manual table creation (use migrations instead)

### `create_superuser_table.py`
**Purpose:** Create legacy superuser table  
**Usage:** `python scripts/create_superuser_table.py`  
**When to use:** Legacy script (replaced by SchoolAnalyticsProfile)

### `drop_avatar_table.py`
**Purpose:** Drop Avatar table (destructive!)  
**Usage:** `python scripts/drop_avatar_table.py`  
**When to use:** Resetting avatar system (CAUTION: deletes all avatar data)

---

## Admin Management

### `create_admin.py`
**Purpose:** Create school admin users  
**Usage:** `python scripts/create_admin.py`  
**When to use:** Setting up school administrators

### `check_admin.py`
**Purpose:** Verify admin user exists  
**Usage:** `python scripts/check_admin.py`  
**When to use:** Troubleshooting admin access issues

### `verify_admin.py`
**Purpose:** Validate admin credentials and permissions  
**Usage:** `python scripts/verify_admin.py`  
**When to use:** Confirming admin setup

### `set_admin_password.py`
**Purpose:** Reset admin password  
**Usage:** `python scripts/set_admin_password.py`  
**When to use:** Password recovery

---

## Testing

### `test_python.py`
**Purpose:** Basic Python environment test  
**Usage:** `python scripts/test_python.py`  
**When to use:** Verifying Python installation and imports

---

## Legacy Development Tools

### `START_DJANGO.bat`
**Purpose:** Windows batch script for starting Django dev server  
**Note:** Contains Cloudinary uninstall workaround for Python 3.14 compatibility  
**Current:** Replaced by `QUICKSTART.md` in project root

### `START_SERVER.ps1`
**Purpose:** PowerShell script for starting Django dev server  
**Note:** Contains Cloudinary uninstall workaround for Python 3.14 compatibility  
**Current:** Replaced by `QUICKSTART.md` in project root

### `widgit-symbols-example.html`
**Purpose:** Example HTML demonstrating Widgit symbol integration  
**When to use:** Reference for accessibility features implementation

**🚀 For current development:** Use [../QUICKSTART.md](../QUICKSTART.md)

---

## Recommended Workflow

**For Production:**
- Use Django management commands: `python manage.py <command>`
- Avoid direct script execution on production databases

**For Development:**
1. Run within virtual environment: `.venv\Scripts\activate`
2. Ensure DATABASE_URL is set correctly in `env.py`
3. Back up database before running database scripts
4. Use migrations over direct schema modification scripts

---

## Safety Notes

⚠️ **Always backup your database before running any script**  
⚠️ **Test on development environment first**  
⚠️ **Review script contents before execution**  

---

**See:** [Main README](../README.md) for installation and setup instructions.
