import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()

# Create the SchoolAnalyticsProfile table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS core_schoolanalyticsprofile (
        id BIGSERIAL PRIMARY KEY,
        teacher_id BIGINT NOT NULL UNIQUE REFERENCES core_user(id) ON DELETE CASCADE,
        school VARCHAR(255) NOT NULL,
        can_access_all_teachers BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    )
""")

print("✅ Created core_schoolanalyticsprofile table successfully")
