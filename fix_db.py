import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()
from django.db import connection

cursor = connection.cursor()

# Add description column to Class if it doesn't exist
try:
    cursor.execute('ALTER TABLE core_class ADD COLUMN description TEXT NULL')
    print('Added description column to core_class')
except Exception as e:
    print(f'Description column already exists or error: {e}')

# Drop old tables that don't exist in new schema
tables_to_drop = ['core_studentprofile', 'core_session', 'core_objectiveattempt', 'core_studentobjectivemastery', 'core_gameevent', 'core_school']

for table in tables_to_drop:
    try:
        cursor.execute(f'DROP TABLE IF EXISTS {table} CASCADE')
        print(f'Dropped {table}')
    except Exception as e:
        print(f'Could not drop {table}: {e}')

print('Database cleanup complete')
