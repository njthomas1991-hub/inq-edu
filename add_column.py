import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.backend.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("ALTER TABLE core_user ADD COLUMN IF NOT EXISTS plain_password VARCHAR(100);")
    print("Column added successfully")
