# Quick Start Guide

> **📖 Full Documentation:** See [README.md](README.md) for complete installation instructions.

## Local Development

### Windows (PowerShell)
```powershell
# 1. Activate virtual environment
.venv\Scripts\activate

# 2. Navigate to backend
cd backend

# 3. Run migrations
python manage.py migrate

# 4. Start server
python manage.py runserver
```

### macOS/Linux (Bash)
```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Navigate to backend
cd backend

# 3. Run migrations
python manage.py migrate

# 4. Start server
python manage.py runserver
```

**Access at:** http://localhost:8000

---

## First Time Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create environment file:**
   - Copy `env.py.example` to `env.py`
   - Set your `SECRET_KEY` and `DATABASE_URL`

3. **Run migrations:**
   ```bash
   python backend/manage.py migrate
   ```

4. **Create superuser (optional):**
   ```bash
   python backend/manage.py createsuperuser
   ```

---

## Troubleshooting

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

**Database issues:**
```bash
# Delete and recreate database
python manage.py flush
python manage.py migrate
```

**Static files not loading:**
```bash
python manage.py collectstatic --noinput
```

---

**For heroku deployment:** See [README.md#deployment](README.md#deployment)
