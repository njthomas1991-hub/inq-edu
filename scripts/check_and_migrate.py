#!/usr/bin/env python
"""Check migration status and run migrations if needed"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Load environment variables from env.py if it exists
env_path = os.path.join(os.path.dirname(__file__), 'env.py')
if os.path.isfile(env_path):
    with open(env_path) as f:
        exec(f.read())

django.setup()

from django.core.management import call_command
from django.db.migrations.executor import MigrationExecutor
from django.db import connections

def check_migrations():
    """Check if there are unapplied migrations"""
    connection = connections['default']
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    plan = executor.migration_plan(targets)
    
    if plan:
        print("Unapplied migrations found:")
        for migration, _ in plan:
            print(f"  - {migration.app_label}.{migration.name}")
        return True
    else:
        print("All migrations are applied.")
        return False

def run_migrations():
    """Run Django migrations"""
    print("\nRunning migrations...")
    call_command('migrate', verbosity=2)
    print("\nMigrations completed successfully!")

if __name__ == '__main__':
    has_unapplied = check_migrations()
    if has_unapplied:
        user_input = input("\nWould you like to apply these migrations? (yes/no): ")
        if user_input.lower() in ['yes', 'y']:
            run_migrations()
        else:
            print("Migrations not applied.")
    
    # Check if Avatar table exists
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='core_avatar';
        """)
        result = cursor.fetchone()
        if result:
            print("\n✓ Avatar table exists in database")
            
            # Count avatars
            cursor.execute("SELECT COUNT(*) FROM core_avatar;")
            count = cursor.fetchone()[0]
            print(f"  Found {count} avatar(s) in database")
        else:
            print("\n✗ Avatar table does NOT exist in database")
            print("  Run migrations to create it!")
