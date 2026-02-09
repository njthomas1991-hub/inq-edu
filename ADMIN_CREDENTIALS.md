# Admin Account Credentials

This file documents the admin/superuser account credentials for the project.

## Default Admin Account

**Username:** `admin`  
**Email:** `admin@example.com`  
**Password:** `admin12345`

## Access

The admin account is created automatically via Django migration (`0021_create_admin_user.py`) when you run:

```bash
python backend/manage.py migrate
```

## Admin Site

Access the Django admin panel at:

```
http://127.0.0.1:8000/admin/
```

Log in with the credentials above.

## Changing Admin Password

To change the admin password, you can:

1. **Via Django Admin Site:**
   - Log in to http://127.0.0.1:8000/admin/
   - Go to Users → admin → Change password

2. **Via Command Line:**
   ```bash
   python backend/manage.py changepassword admin
   ```

3. **Via Django Shell:**
   ```bash
   python backend/manage.py shell
   ```
   Then run:
   ```python
   from core.models import User
   user = User.objects.get(username='admin')
   user.set_password('new_password')
   user.save()
   ```

## Database Storage

The admin user is stored in the PostgreSQL database (Neon) with full superuser permissions:
- **is_staff:** True
- **is_superuser:** True
- **is_active:** True
- **role:** teacher

This ensures the admin account persists across server restarts and deployments.
