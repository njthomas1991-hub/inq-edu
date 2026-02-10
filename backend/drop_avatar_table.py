#!/usr/bin/env python
"""Drop the Avatar table and recreate with new schema"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Load environment variables from env.py if it exists
env_path = os.path.join(os.path.dirname(__file__), 'env.py')
if os.path.isfile(env_path):
    with open(env_path) as f:
        exec(f.read())

django.setup()

from django.db import connection

with connection.cursor() as cursor:
    try:
        cursor.execute("DROP TABLE IF EXISTS core_avatar CASCADE;")
        print("✓ Avatar table dropped successfully")
        connection.commit()
    except Exception as e:
        print(f"✗ Error dropping table: {e}")
        connection.rollback()
