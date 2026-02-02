#!/bin/bash
export PYTHONPATH=/app/backend:$PYTHONPATH
python manage.py migrate
exec gunicorn --bind 0.0.0.0:$PORT backend.wsgi:application
