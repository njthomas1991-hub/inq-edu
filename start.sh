#!/bin/bash
echo "=== DEBUG: Listing /app contents ==="
ls -la /app | head -20
echo "=== DEBUG: Listing /app/backend contents ==="
ls -la /app/backend 2>/dev/null || echo "backend directory not found"
echo "=== DEBUG: PYTHONPATH is: $PYTHONPATH ==="
export PYTHONPATH=/app/backend:$PYTHONPATH
python manage.py migrate
exec gunicorn --bind 0.0.0.0:$PORT backend.wsgi:application
