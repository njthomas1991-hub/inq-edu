# Local HTTPS Setup for Development

## Why You See "Not Secure" Warning

Chrome shows this for any HTTP (not HTTPS) connection. For `localhost` development, this is **totally safe** - your data never leaves your computer.

## Option 1: Ignore the Warning (Recommended for Development)

In Chrome, you can:
1. Type `thisisunsafe` while on the page (Chrome easter egg - just type it, no input field needed)
2. Or click "Advanced" → "Proceed to localhost (unsafe)"

This is the standard approach for local development.

## Option 2: Enable HTTPS on Django Development Server

If you really want HTTPS:

### Step 1: Install django-extensions
```powershell
pip install django-extensions werkzeug pyOpenSSL
```

### Step 2: Add to settings.py INSTALLED_APPS
```python
INSTALLED_APPS = [
    # ... existing apps ...
    'django_extensions',
]
```

### Step 3: Run with SSL
```powershell
python manage.py runserver_plus --cert-file cert.crt
```

This generates a self-signed certificate (browser will still warn, but you can accept it).

## Option 3: Use mkcert for Trusted Certificates (Best for HTTPS)

### Install mkcert
```powershell
# Using Chocolatey
choco install mkcert

# Or download from: https://github.com/FiloSottile/mkcert/releases
```

### Generate certificates
```powershell
# Install local CA
mkcert -install

# Generate certificate for localhost
cd D:\vs-projects\inq-ed\myproject\backend
mkcert localhost 127.0.0.1 ::1
```

This creates:
- `localhost+2.pem` (certificate)
- `localhost+2-key.pem` (private key)

### Run Django with HTTPS
```powershell
python manage.py runserver_plus --cert-file localhost+2.pem --key-file localhost+2-key.pem
```

### Access at
```
https://localhost:8000
```

---

## For Production (When Deploying)

For production on Heroku/Railway/etc, use:
- Heroku: Automatic HTTPS with their SSL certificates
- Let's Encrypt: Free SSL certificates
- Cloudflare: Free SSL proxy

**In `settings.py` for production:**
```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

## Recommended Approach

**For local development:** Just ignore the warning - it's meaningless on localhost.

**For production:** Use your hosting platform's SSL solution (Heroku, Railway, etc. provide this automatically).
