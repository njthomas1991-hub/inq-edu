import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()
from django.db import connection

cursor = connection.cursor()

# Rename clazz_id to class_obj_id in core_classstudent
try:
    cursor.execute('ALTER TABLE core_classstudent RENAME COLUMN clazz_id TO class_obj_id')
    print('Renamed clazz_id to class_obj_id')
except Exception as e:
    print(f'Could not rename clazz_id: {e}')

# Check if student_id points to core_studentprofile (old) or core_user (new)
try:
    cursor.execute("""
        SELECT constraint_name 
        FROM information_schema.table_constraints 
        WHERE table_name = 'core_classstudent' 
        AND constraint_type = 'FOREIGN KEY'
    """)
    constraints = cursor.fetchall()
    print(f'Found constraints: {constraints}')
    
    # Drop old foreign key constraint pointing to core_studentprofile
    for constraint in constraints:
        try:
            cursor.execute(f'ALTER TABLE core_classstudent DROP CONSTRAINT {constraint[0]}')
            print(f'Dropped constraint: {constraint[0]}')
        except Exception as e:
            print(f'Could not drop constraint {constraint[0]}: {e}')
    
    # Add new foreign key constraint pointing to core_user
    cursor.execute('ALTER TABLE core_classstudent ADD CONSTRAINT core_classstudent_student_fk FOREIGN KEY (student_id) REFERENCES core_user(id)')
    print('Added new foreign key constraint for student_id -> core_user')
except Exception as e:
    print(f'Error updating foreign key: {e}')

print('Database fix complete')
